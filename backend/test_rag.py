#!/usr/bin/env python3
"""
Test script to verify the RAG system is working properly with book content
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag import rag_service
from vector_store import qdrant_service
from database import SessionLocal, Document

async def test_rag_system():
    """
    Test the RAG system with sample queries
    """
    print("Testing RAG System...")
    print("="*50)
    
    # Check if services are connected
    print(f"Qdrant Connected: {qdrant_service.connected}")
    print(f"Qdrant Collection: {os.getenv('QDRANT_COLLECTION_NAME', 'book_embeddings')}")
    
    # Check database
    db = SessionLocal()
    try:
        doc_count = db.query(Document).count()
        print(f"Documents in database: {doc_count}")
        
        if doc_count > 0:
            sample_docs = db.query(Document).limit(2).all()
            print("Sample documents:")
            for doc in sample_docs:
                print(f"  - {doc.title} (Section: {doc.section})")
    finally:
        db.close()
    
    print("\n" + "="*50)
    
    # Test queries
    test_queries = [
        "What is Physical AI?",
        "Explain humanoid robotics",
        "What are the key concepts in the introduction?",
        "Tell me about ROS2 fundamentals"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nTest Query {i}: {query}")
        print("-" * 30)
        
        try:
            response = await rag_service.query(query)
            print(f"Response: {response.response[:500]}{'...' if len(response.response) > 500 else ''}")
            print(f"Sources: {len(response.sources)} documents referenced")
            
            if response.sources:
                print("Top source snippets:")
                for idx, source in enumerate(response.sources[:2]):  # Show first 2 sources
                    snippet = source.get('text', '')[:200]
                    print(f"  {idx+1}. {snippet}{'...' if len(snippet) == 200 else ''}")
                    
        except Exception as e:
            print(f"Error processing query: {e}")
            import traceback
            traceback.print_exc()

async def main():
    print("RAG System Test Suite")
    print("="*60)
    
    await test_rag_system()
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("If the system responded to queries, it's working properly!")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())