import os
import sys
from pathlib import Path
import asyncio
from typing import List, Dict, Any

# Add the backend directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, Document
from vector_store import qdrant_service
from main import chunk_document
from datetime import datetime

async def index_book_content():
    """
    Index the entire book content from the frontend documentation into the RAG system
    """
    print("Starting book content indexing...")
    
    # Define the base path for the frontend docs
    frontend_docs_path = Path("../frontend/docs")
    
    if not frontend_docs_path.exists():
        print(f"Frontend docs path does not exist: {frontend_docs_path}")
        return False
    
    # Get all markdown files in the docs directory and subdirectories
    md_files = list(frontend_docs_path.rglob("*.md"))
    
    print(f"Found {len(md_files)} markdown files to process")
    
    for md_file in md_files:
        try:
            print(f"Processing: {md_file}")
            
            # Read the file content
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract metadata from the file (title, etc.)
            title = extract_title_from_content(content)
            section = md_file.parent.name  # Use the directory name as section
            doc_id = str(md_file.relative_to(frontend_docs_path)).replace('/', '_').replace('\\', '_').replace('.md', '')
            
            # Remove frontmatter from content if present
            processed_content = remove_frontmatter(content)
            
            # Chunk the document
            chunks = chunk_document(processed_content)
            print(f"  - Created {len(chunks)} content chunks")
            
            # Store document metadata in the database
            db = SessionLocal()
            try:
                # Check if document already exists
                existing_doc = db.query(Document).filter(Document.doc_id == doc_id).first()
                
                if existing_doc:
                    print(f"  - Document {doc_id} already indexed, skipping")
                    # We could update it instead if needed
                else:
                    # Create new document entry
                    doc = Document(
                        doc_id=doc_id,
                        title=title,
                        content=processed_content,
                        section=section,
                        is_indexed=True,
                        created_at=datetime.utcnow()
                    )
                    db.add(doc)
                    db.commit()
                    print(f"  - Added document to database: {title}")
            except Exception as e:
                print(f"  - Error adding document to database: {e}")
                db.rollback()
            finally:
                db.close()
            
            # Store embeddings in Qdrant
            if chunks:
                doc_ids = [doc_id] * len(chunks)
                metadata_list = [{"section": section, "title": title} for _ in chunks]
                
                try:
                    vector_ids = await qdrant_service.store_embeddings(chunks, doc_ids, metadata_list)
                    print(f"  - Stored {len(vector_ids)} embeddings in vector store")
                    
                    # Update document record with embedding reference
                    db = SessionLocal()
                    try:
                        doc = db.query(Document).filter(Document.doc_id == doc_id).first()
                        if doc:
                            doc.embedding_vector_id = ",".join(vector_ids)
                            doc.updated_at = datetime.utcnow()
                            db.commit()
                            print(f"  - Updated document with vector IDs")
                    except Exception as e:
                        print(f"  - Error updating document with vector IDs: {e}")
                        db.rollback()
                    finally:
                        db.close()
                except Exception as e:
                    print(f"  - Error storing embeddings in vector store: {e}")
            
        except Exception as e:
            print(f"Error processing file {md_file}: {e}")
            continue
    
    print("Book content indexing completed!")
    return True

def extract_title_from_content(content: str) -> str:
    """
    Extract title from content, handling frontmatter if present
    """
    lines = content.split('\n')
    
    # Look for title in frontmatter first
    if lines and lines[0].strip() == '---':
        in_frontmatter = True
        for line in lines[1:]:
            if line.strip() == '---':
                # End of frontmatter
                break
            if line.strip().startswith('title:'):
                title = line.split('title:', 1)[1].strip().strip('"\'')
                return title
    
    # If no title in frontmatter, look for first heading
    for line in lines:
        if line.strip().startswith('# '):
            return line.strip('# ').strip()
    
    # If no title found, return generic title
    return "Untitled Document"

def remove_frontmatter(content: str) -> str:
    """
    Remove frontmatter from content if present
    """
    lines = content.split('\n')
    
    if len(lines) > 1 and lines[0].strip() == '---':
        # Find the end of frontmatter
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == '---':
                # Return content after frontmatter
                return '\n'.join(lines[i+1:])
    
    # If no frontmatter, return original content
    return content

if __name__ == "__main__":
    success = asyncio.run(index_book_content())
    if success:
        print("Successfully indexed book content!")
    else:
        print("Failed to index book content.")