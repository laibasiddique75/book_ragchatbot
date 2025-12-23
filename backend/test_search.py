import asyncio
from vector_store import qdrant_service

async def test_search():
    print("Testing search functionality...")
    
    # Test searching for a specific term that should exist in the content
    results = await qdrant_service.search_similar("Why Physical AI", limit=5)
    print(f"Found {len(results)} results for 'Why Physical AI'")
    
    for i, result in enumerate(results):
        print(f"Result {i+1}: Score={result['score']}")
        print(f"Text preview: {result['text'][:200]}...")
        print("---")
    
    # Also test a broader search
    results2 = await qdrant_service.search_similar("Physical AI", limit=5)
    print(f"\nFound {len(results2)} results for 'Physical AI'")
    
    for i, result in enumerate(results2):
        print(f"Result {i+1}: Score={result['score']}")
        print(f"Text preview: {result['text'][:200]}...")
        print("---")

if __name__ == "__main__":
    asyncio.run(test_search())