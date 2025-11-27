"""
Test script for READ operation - Querying and retrieving embeddings from ChromaDB
"""
import sys
from pathlib import Path

# Add parent directories to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from db.chromadb_service import ChromaDBService
from utils import text_to_embeddings

def test_read_all():
    """Test reading all embeddings"""
    print("=" * 60)
    print("Testing READ Operation - Get All")
    print("=" * 60)
    
    db = ChromaDBService(collection_name="test_collection")
    
    # Get all entries
    results = db.read()
    
    print(f"\n📖 Found {len(results['ids'])} entries in collection")
    
    for i, (doc_id, doc) in enumerate(zip(results['ids'], results['documents']), 1):
        metadata = results['metadatas'][i-1] if results['metadatas'] else {}
        print(f"\n{i}. ID: {doc_id}")
        print(f"   Text: {doc[:80]}...")
        if metadata:
            print(f"   Metadata: {metadata}")
    
    print("\n" + "=" * 60)
    print("✅ READ ALL test completed!")
    print("=" * 60)

def test_read_by_ids():
    """Test reading specific entries by IDs"""
    print("\n" + "=" * 60)
    print("Testing READ Operation - Get by IDs")
    print("=" * 60)
    
    db = ChromaDBService(collection_name="test_collection")
    
    # Get specific entries
    target_ids = ["doc_001", "doc_003"]
    results = db.read(ids=target_ids)
    
    print(f"\n📖 Retrieved {len(results['ids'])} entries by IDs")
    
    for doc_id, doc in zip(results['ids'], results['documents']):
        print(f"\n   ID: {doc_id}")
        print(f"   Text: {doc}")
    
    print("\n" + "=" * 60)
    print("✅ READ BY ID test completed!")
    print("=" * 60)

def test_read_by_text_query():
    """Test semantic search using text queries"""
    print("\n" + "=" * 60)
    print("Testing READ Operation - Text Query (Semantic Search)")
    print("=" * 60)
    
    db = ChromaDBService(collection_name="test_collection")
    
    # Search using text query
    query = "programming language"
    print(f"\n🔍 Searching for: '{query}'")
    
    results = db.read(
        query_texts=[query],
        n_results=3
    )
    
    print(f"\n📖 Found {len(results['ids'])} similar entries")
    
    for i, (doc_id, doc, distance) in enumerate(
        zip(results['ids'][0], results['documents'][0], results['distances'][0]), 
        1
    ):
        print(f"\n{i}. ID: {doc_id}")
        print(f"   Text: {doc}")
        print(f"   Similarity Distance: {distance:.4f} (lower = more similar)")
    
    print("\n" + "=" * 60)
    print("✅ TEXT QUERY test completed!")
    print("=" * 60)

def test_read_by_embedding():
    """Test search using embedding vectors"""
    print("\n" + "=" * 60)
    print("Testing READ Operation - Embedding Vector Search")
    print("=" * 60)
    
    db = ChromaDBService(collection_name="test_collection")
    
    # Generate embedding for query
    query_text = "vector database"
    print(f"\n🔍 Searching with embedding for: '{query_text}'")
    
    query_embeddings = text_to_embeddings([query_text])
    
    results = db.read(
        query_embeddings=query_embeddings,
        n_results=2
    )
    
    print(f"\n📖 Found {len(results['ids'][0])} similar entries")
    
    for i, (doc_id, doc, distance) in enumerate(
        zip(results['ids'][0], results['documents'][0], results['distances'][0]), 
        1
    ):
        print(f"\n{i}. ID: {doc_id}")
        print(f"   Text: {doc}")
        print(f"   Distance: {distance:.4f}")
    
    print("\n" + "=" * 60)
    print("✅ EMBEDDING SEARCH test completed!")
    print("=" * 60)

def test_read_with_metadata_filter():
    """Test reading with metadata filters"""
    print("\n" + "=" * 60)
    print("Testing READ Operation - Metadata Filter")
    print("=" * 60)
    
    db = ChromaDBService(collection_name="test_collection")
    
    # Search with metadata filter
    print(f"\n🔍 Searching with metadata filter: category='programming'")
    
    results = db.read(
        query_texts=["programming"],
        n_results=5,
        where={"category": "programming"}
    )
    
    print(f"\n📖 Found {len(results['ids'][0])} entries matching filter")
    
    for i, (doc_id, doc, metadata) in enumerate(
        zip(results['ids'][0], results['documents'][0], results['metadatas'][0]), 
        1
    ):
        print(f"\n{i}. ID: {doc_id}")
        print(f"   Text: {doc}")
        print(f"   Metadata: {metadata}")
    
    print("\n" + "=" * 60)
    print("✅ METADATA FILTER test completed!")
    print("=" * 60)

if __name__ == "__main__":
    print("\n⚠️  Make sure you've run test_create.py first to populate the database!\n")
    
    test_read_all()
    test_read_by_ids()
    test_read_by_text_query()
    test_read_by_embedding()
    test_read_with_metadata_filter()
    
    print("\n" + "=" * 60)
    print("✅ All READ tests completed!")
    print("=" * 60)

