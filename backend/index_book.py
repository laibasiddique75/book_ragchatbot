import os
import sys
import asyncio
from pathlib import Path

# Add the backend directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import chunk_document
from vector_store import qdrant_service
from database import SessionLocal, Document
from datetime import datetime

def read_book_content():
    """Read the book content from the frontend docs directory"""
    # Define the paths to the book content
    book_dir = Path("../frontend/docs")
    content_files = [
        "intro.md",
        "introduction/why-physical-ai.md",
        "ros2-fundamentals/week-3-5.md",
        "lab-setup/digital-twin-workstation.md"
    ]
    
    all_content = []
    
    for file_path in content_files:
        full_path = book_dir / file_path
        if full_path.exists():
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract title from the content (first line after metadata)
                lines = content.split('\n')
                title = "Untitled"
                content_body = content
                if lines and lines[0].startswith('---'):
                    # Skip metadata section
                    for i, line in enumerate(lines[1:], 1):
                        if line.startswith('---'):
                            # End of metadata
                            content_body = '\n'.join(lines[i+1:])
                            # Look for title in metadata
                            for j in range(1, i):  # Check lines in metadata
                                if 'title:' in lines[j]:
                                    title = lines[j].split('title:', 1)[1].strip().strip('"\'')
                            break
                
                # Create document entry
                doc_entry = {
                    'title': title,
                    'content': content_body,
                    'doc_id': file_path.replace('/', '_').replace('.md', ''),
                    'section': file_path.split('/')[0] if '/' in file_path else 'intro'
                }
                all_content.append(doc_entry)
        else:
            print(f"File not found: {full_path}")
    
    return all_content

async def index_book_content():
    """Index the book content into the database and vector store"""
    print("Starting book content indexing...")
    
    # Read all book content
    book_content = read_book_content()
    print(f"Found {len(book_content)} documents to index")
    
    for doc_data in book_content:
        print(f"Indexing: {doc_data['title']} (ID: {doc_data['doc_id']})")
        
        # Chunk the document content
        chunks = chunk_document(doc_data['content'])
        print(f"  - Created {len(chunks)} chunks")
        
        # Store document metadata in database
        db = SessionLocal()
        try:
            # Check if document already exists
            existing_doc = db.query(Document).filter(Document.doc_id == doc_data['doc_id']).first()
            if existing_doc:
                print(f"  - Document {doc_data['doc_id']} already exists, skipping database entry")
            else:
                # Create document record
                doc = Document(
                    doc_id=doc_data['doc_id'],
                    title=doc_data['title'],
                    content=doc_data['content'],
                    section=doc_data['section'],
                    is_indexed=True,
                    created_at=datetime.utcnow()
                )
                db.add(doc)
                db.commit()
                print(f"  - Added document to database")
        except Exception as e:
            print(f"  - Error adding document to database: {e}")
            db.rollback()
        finally:
            db.close()
        
        # Store embeddings in Qdrant
        if chunks:
            doc_ids = [doc_data['doc_id']] * len(chunks)
            metadata_list = [{"section": doc_data['section'], "title": doc_data['title']} for _ in chunks]
            
            try:
                vector_ids = await qdrant_service.store_embeddings(chunks, doc_ids, metadata_list)
                print(f"  - Stored {len(vector_ids)} embeddings in vector store")
                
                # Update document record with embedding reference
                db = SessionLocal()
                try:
                    doc = db.query(Document).filter(Document.doc_id == doc_data['doc_id']).first()
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
    
    print("Book content indexing completed!")

if __name__ == "__main__":
    asyncio.run(index_book_content())