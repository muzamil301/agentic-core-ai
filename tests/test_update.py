"""
Test script for UPDATE operation - Updating existing embeddings in ChromaDB
"""
from db.chromadb_service import ChromaDBService
from utils import text_to_embeddings

def test_update_text_and_embedding():
    """Test updating both text and embedding"""
    print("=" * 60)
    print("Testing UPDATE Operation - Text and Embedding")
    print("=" * 60)
    
    db = ChromaDBService(collection_name="test_collection")
    
    # First, read the existing entry
    print("\n📖 Reading existing entry...")
    existing = db.read(ids=["doc_001"])
    
    if not existing['ids']:
        print("❌ Entry 'doc_001' not found. Run test_create.py first!")
        return
    
    print(f"   Original text: {existing['documents'][0]}")
    print(f"   Original metadata: {existing['metadatas'][0]}")
    
    # Update with new text and embedding
    new_text = "Python is a high-level, interpreted programming language used for web development, data science, and AI"
    print(f"\n✏️  Updating to: {new_text}")
    
    new_embedding = text_to_embeddings([new_text])[0]
    
    db.update(
        ids=["doc_001"],
        texts=[new_text],
        embeddings=[new_embedding],
        metadatas=[{"category": "programming", "topic": "python", "updated": True}]
    )
    
    # Verify update
    print("\n✅ Update completed. Verifying...")
    updated = db.read(ids=["doc_001"])
    print(f"   Updated text: {updated['documents'][0]}")
    print(f"   Updated metadata: {updated['metadatas'][0]}")
    
    print("\n" + "=" * 60)
    print("✅ UPDATE test completed!")
    print("=" * 60)

def test_update_text_only():
    """Test updating only text (embedding will be preserved)"""
    print("\n" + "=" * 60)
    print("Testing UPDATE Operation - Text Only")
    print("=" * 60)
    
    db = ChromaDBService(collection_name="test_collection")
    
    # Read existing entry
    print("\n📖 Reading existing entry...")
    existing = db.read(ids=["doc_002"])
    
    if not existing['ids']:
        print("❌ Entry 'doc_002' not found. Run test_create.py first!")
        return
    
    original_embedding = existing['embeddings'][0]
    print(f"   Original text: {existing['documents'][0]}")
    
    # Update only text (embedding preserved)
    new_text = "ChromaDB is an open-source vector database optimized for AI applications and semantic search"
    print(f"\n✏️  Updating text to: {new_text}")
    print("   (Embedding will be preserved from original)")
    
    db.update(
        ids=["doc_002"],
        texts=[new_text]
        # embeddings and metadatas not provided - will use existing
    )
    
    # Verify update
    print("\n✅ Update completed. Verifying...")
    updated = db.read(ids=["doc_002"])
    print(f"   Updated text: {updated['documents'][0]}")
    print(f"   Embedding preserved: {len(updated['embeddings'][0]) == len(original_embedding)}")
    
    print("\n" + "=" * 60)
    print("✅ UPDATE TEXT ONLY test completed!")
    print("=" * 60)

def test_update_metadata_only():
    """Test updating only metadata"""
    print("\n" + "=" * 60)
    print("Testing UPDATE Operation - Metadata Only")
    print("=" * 60)
    
    db = ChromaDBService(collection_name="test_collection")
    
    # Read existing entry
    print("\n📖 Reading existing entry...")
    existing = db.read(ids=["doc_003"])
    
    if not existing['ids']:
        print("❌ Entry 'doc_003' not found. Run test_create.py first!")
        return
    
    print(f"   Original metadata: {existing['metadatas'][0]}")
    
    # Update only metadata
    new_metadata = {
        "category": "ai",
        "topic": "embeddings",
        "subtopic": "semantic_search",
        "updated": True,
        "version": "2.0"
    }
    print(f"\n✏️  Updating metadata to: {new_metadata}")
    
    db.update(
        ids=["doc_003"],
        metadatas=[new_metadata]
        # texts and embeddings not provided - will use existing
    )
    
    # Verify update
    print("\n✅ Update completed. Verifying...")
    updated = db.read(ids=["doc_003"])
    print(f"   Updated metadata: {updated['metadatas'][0]}")
    print(f"   Text preserved: {updated['documents'][0][:60]}...")
    
    print("\n" + "=" * 60)
    print("✅ UPDATE METADATA ONLY test completed!")
    print("=" * 60)

def test_update_multiple_entries():
    """Test updating multiple entries at once"""
    print("\n" + "=" * 60)
    print("Testing UPDATE Operation - Multiple Entries")
    print("=" * 60)
    
    db = ChromaDBService(collection_name="test_collection")
    
    # Read existing entries
    print("\n📖 Reading existing entries...")
    existing = db.read(ids=["doc_001", "doc_002"])
    
    if len(existing['ids']) < 2:
        print("❌ Not enough entries found. Run test_create.py first!")
        return
    
    # Update multiple entries
    new_texts = [
        "Updated: Python programming language",
        "Updated: ChromaDB vector database"
    ]
    new_embeddings = text_to_embeddings(new_texts)
    new_metadatas = [
        {"category": "programming", "updated": True, "batch": 1},
        {"category": "database", "updated": True, "batch": 1}
    ]
    
    print(f"\n✏️  Updating {len(new_texts)} entries...")
    
    db.update(
        ids=["doc_001", "doc_002"],
        texts=new_texts,
        embeddings=new_embeddings,
        metadatas=new_metadatas
    )
    
    # Verify updates
    print("\n✅ Updates completed. Verifying...")
    updated = db.read(ids=["doc_001", "doc_002"])
    
    for i, (doc_id, doc, metadata) in enumerate(
        zip(updated['ids'], updated['documents'], updated['metadatas']), 
        1
    ):
        print(f"\n{i}. ID: {doc_id}")
        print(f"   Text: {doc}")
        print(f"   Metadata: {metadata}")
    
    print("\n" + "=" * 60)
    print("✅ UPDATE MULTIPLE test completed!")
    print("=" * 60)

if __name__ == "__main__":
    print("\n⚠️  Make sure you've run test_create.py first to populate the database!\n")
    
    test_update_text_and_embedding()
    test_update_text_only()
    test_update_metadata_only()
    test_update_multiple_entries()
    
    print("\n" + "=" * 60)
    print("✅ All UPDATE tests completed!")
    print("=" * 60)

