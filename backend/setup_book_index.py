#!/usr/bin/env python3
"""
Setup script to properly index the book content into the RAG system
"""
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
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

async def index_book_content():
    """
    Index the entire book content from the frontend documentation into the RAG system
    """
    print("Starting comprehensive book content indexing...")

    # Define the base path for the frontend docs (relative to backend directory)
    frontend_docs_path = Path("../frontend/docs")

    if not frontend_docs_path.exists():
        print(f"ERROR: Frontend docs path does not exist: {frontend_docs_path}")
        print("Make sure you have the book content in the frontend/docs directory")
        return False

    # Get all markdown files in the docs directory and subdirectories
    md_files = list(frontend_docs_path.rglob("*.md"))

    if not md_files:
        print(f"No markdown files found in {frontend_docs_path}")
        return False

    print(f"Found {len(md_files)} markdown files to process")

    total_chunks_stored = 0

    for md_file in md_files:
        try:
            print(f"\nProcessing: {md_file}")

            # Read the file content
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract metadata from the file (title, etc.)
            title = extract_title_from_content(content)
            section = str(md_file.parent.name)  # Use the directory name as section
            doc_id = str(md_file.relative_to(frontend_docs_path)).replace('/', '_').replace('\\', '_').replace('.md', '')

            # Remove frontmatter from content if present
            processed_content = remove_frontmatter(content)

            # Chunk the document
            chunks = chunk_document(processed_content, chunk_size=1000, overlap=100)
            print(f"  - Created {len(chunks)} content chunks")

            # Store document metadata in the database
            db = SessionLocal()
            try:
                # Check if document already exists
                existing_doc = db.query(Document).filter(Document.doc_id == doc_id).first()

                if existing_doc:
                    print(f"  - Document {doc_id} already indexed, updating...")
                    # Update existing document
                    existing_doc.title = title
                    existing_doc.content = processed_content
                    existing_doc.section = section
                    existing_doc.is_indexed = True
                    existing_doc.updated_at = datetime.utcnow()
                    db.commit()
                    print(f"  - Updated document in database: {title}")
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
                print(f"  - ERROR adding document to database: {e}")
                db.rollback()
                continue
            finally:
                db.close()

            # Store embeddings in Qdrant
            if chunks:
                doc_ids = [doc_id] * len(chunks)
                metadata_list = [{"section": section, "title": title, "file_path": str(md_file)} for _ in chunks]

                try:
                    vector_ids = await qdrant_service.store_embeddings(chunks, doc_ids, metadata_list)
                    print(f"  - Stored {len(vector_ids)} embeddings in vector store")
                    total_chunks_stored += len(vector_ids)

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
                        print(f"  - ERROR updating document with vector IDs: {e}")
                        db.rollback()
                    finally:
                        db.close()
                except Exception as e:
                    print(f"  - ERROR storing embeddings in vector store: {e}")
                    print(f"    This may be due to Qdrant connection issues or rate limits")
            else:
                print(f"  - No chunks to store for this document")

        except FileNotFoundError:
            print(f"ERROR: File not found: {md_file}")
            continue
        except UnicodeDecodeError:
            print(f"ERROR: Could not decode file (encoding issue): {md_file}")
            continue
        except Exception as e:
            print(f"ERROR processing file {md_file}: {e}")
            import traceback
            traceback.print_exc()
            continue

    print(f"\nBook content indexing completed!")
    print(f"Total chunks stored in vector database: {total_chunks_stored}")

    # Verify the connection status
    if qdrant_service.connected:
        print("[OK] Successfully connected to Qdrant vector database")
    else:
        print("[WARN] Warning: Could not connect to Qdrant vector database")
        print("  Book content was stored in the SQL database but not in the vector store")
        print("  The RAG system will not be able to retrieve context without a vector store")

    return True

async def verify_indexing():
    """
    Verify that the book content has been properly indexed
    """
    print("\nVerifying indexing status...")

    db = SessionLocal()
    try:
        doc_count = db.query(Document).count()
        print(f"Documents in database: {doc_count}")

        if doc_count > 0:
            sample_docs = db.query(Document).limit(3).all()
            print("Sample documents:")
            for doc in sample_docs:
                print(f"  - ID: {doc.doc_id}, Title: {doc.title}, Section: {doc.section}")

        # Check vector store connection
        if qdrant_service.connected:
            try:
                # Try to get collection info
                collections = qdrant_service.client.get_collections()
                print(f"Qdrant collections: {[col.name for col in collections.collections]}")

                # Try to count points in the collection
                collection_name = os.getenv("QDRANT_COLLECTION_NAME", "book_embeddings")
                try:
                    count = qdrant_service.client.count(collection_name=collection_name)
                    print(f"Vectors in collection '{collection_name}': {count.count}")
                except Exception as e:
                    print(f"Could not count vectors in collection: {e}")

            except Exception as e:
                print(f"Error checking Qdrant status: {e}")
        else:
            print("Qdrant not connected - vector store is not available")

    finally:
        db.close()

async def main():
    """
    Main function to run the indexing process
    """
    print("="*60)
    print("PHYSICAL AI & HUMANOID ROBOTICS BOOK INDEXING SETUP")
    print("="*60)

    # Check environment variables
    print("\nChecking environment variables...")
    required_vars = ["GOOGLE_API_KEY"]
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"[WARN] Missing required environment variables: {missing_vars}")
        print("Please set these in your .env file before proceeding")
        return False
    else:
        print("[OK] All required environment variables are set")

    # Index the book content
    success = await index_book_content()

    if success:
        print("\n[OK] Book content indexing completed successfully!")

        # Verify the indexing
        await verify_indexing()

        print("\n" + "="*60)
        print("INDEXING COMPLETE - RAG SYSTEM READY")
        print("="*60)
        print("You can now start the main API server with 'python main.py'")
        print("The chatbot will now answer questions based on the book content")
        print("="*60)
    else:
        print("\n[X] Book content indexing failed!")
        print("Check the error messages above and try again")
        return False

    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    if not success:
        sys.exit(1)