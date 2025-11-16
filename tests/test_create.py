"""
Test script for CREATE operation - Writing embeddings to ChromaDB
"""
from db.chromadb_service import ChromaDBService
from utils import text_to_embeddings

def test_create_embeddings():
    """Test creating embeddings in ChromaDB"""
    print("=" * 60)
    print("Testing CREATE Operation")
    print("=" * 60)
    
    # Initialize service
    db = ChromaDBService(collection_name="test_collection")
    
    # Sample texts to embed
    texts = [
        "Python is a versatile programming language",
        "ChromaDB is a vector database for embeddings",
        "Machine learning models use embeddings for semantic search"
    ]
    
    print(f"\n📝 Generating embeddings for {len(texts)} texts...")
    embeddings = text_to_embeddings(texts)
    print(f"✅ Generated {len(embeddings)} embeddings")
    
    # Create with custom IDs
    custom_ids = ["doc_001", "doc_002", "doc_003"]
    metadatas = [
        {"category": "programming", "topic": "python"},
        {"category": "database", "topic": "chromadb"},
        {"category": "ai", "topic": "embeddings"}
    ]
    
    print(f"\n💾 Storing embeddings in ChromaDB...")
    created_ids = db.create(
        texts=texts,
        embeddings=embeddings,
        ids=custom_ids,
        metadatas=metadatas
    )
    
    print(f"✅ Successfully created {len(created_ids)} embeddings")
    print(f"   IDs: {created_ids}")
    
    # Verify by getting collection info
    info = db.get_info()
    print(f"\n📊 Collection Info:")
    print(f"   Collection: {info['collection_name']}")
    print(f"   Total entries: {info['count']}")
    
    print("\n" + "=" * 60)
    print("✅ CREATE test completed successfully!")
    print("=" * 60)
    
    return created_ids

if __name__ == "__main__":
    test_create_embeddings()

