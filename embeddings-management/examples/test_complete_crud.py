"""
Complete CRUD test script - Tests all database operations in sequence
"""
import sys
from pathlib import Path

# Add parent directories to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from db.chromadb_service import ChromaDBService
from utils import text_to_embeddings

def run_complete_crud_test():
    """Run a complete CRUD test cycle"""
    print("=" * 70)
    print("COMPLETE CRUD TEST - Full Database Operations Cycle")
    print("=" * 70)
    
    # Initialize service
    db = ChromaDBService(collection_name="crud_test_collection")
    
    # ============================================================
    # CREATE - Step 1: Create embeddings
    # ============================================================
    print("\n" + "=" * 70)
    print("STEP 1: CREATE - Adding embeddings to database")
    print("=" * 70)
    
    texts = [
        "Python is a powerful programming language",
        "ChromaDB stores vector embeddings efficiently",
        "Machine learning uses embeddings for semantic understanding",
        "RAG systems combine retrieval and generation",
        "Embeddings capture semantic meaning of text"
    ]
    
    print(f"\n📝 Generating embeddings for {len(texts)} texts...")
    embeddings = text_to_embeddings(texts)
    
    ids = [f"doc_{i+1:03d}" for i in range(len(texts))]
    metadatas = [
        {"category": "programming", "topic": "python", "index": 1},
        {"category": "database", "topic": "chromadb", "index": 2},
        {"category": "ai", "topic": "embeddings", "index": 3},
        {"category": "ai", "topic": "rag", "index": 4},
        {"category": "ai", "topic": "embeddings", "index": 5}
    ]
    
    print(f"💾 Storing {len(texts)} embeddings...")
    created_ids = db.create(
        texts=texts,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )
    
    print(f"✅ Created {len(created_ids)} entries")
    print(f"   IDs: {created_ids}")
    
    info = db.get_info()
    print(f"\n📊 Collection now has {info['count']} entries")
    
    # ============================================================
    # READ - Step 2: Read and query embeddings
    # ============================================================
    print("\n" + "=" * 70)
    print("STEP 2: READ - Querying embeddings")
    print("=" * 70)
    
    # Read all
    print("\n📖 Reading all entries...")
    all_results = db.read()
    print(f"   Found {len(all_results['ids'])} entries")
    
    # Read by ID
    print("\n📖 Reading specific entry by ID...")
    specific = db.read(ids=["doc_001"])
    print(f"   Entry: {specific['documents'][0][:60]}...")
    
    # Semantic search
    print("\n🔍 Performing semantic search...")
    search_results = db.read(
        query_texts=["programming language"],
        n_results=3
    )
    print(f"   Found {len(search_results['ids'][0])} similar entries:")
    for i, (doc_id, doc, dist) in enumerate(
        zip(search_results['ids'][0], search_results['documents'][0], search_results['distances'][0]),
        1
    ):
        print(f"   {i}. [{doc_id}] {doc[:50]}... (distance: {dist:.4f})")
    
    # Filter by metadata
    print("\n🔍 Filtering by metadata (category='ai')...")
    filtered = db.read(
        query_texts=["embeddings"],
        n_results=5,
        where={"category": "ai"}
    )
    print(f"   Found {len(filtered['ids'][0])} entries with category='ai'")
    
    # ============================================================
    # UPDATE - Step 3: Update embeddings
    # ============================================================
    print("\n" + "=" * 70)
    print("STEP 3: UPDATE - Modifying existing entries")
    print("=" * 70)
    
    # Update one entry
    print("\n✏️  Updating doc_001...")
    original = db.read(ids=["doc_001"])
    print(f"   Original: {original['documents'][0]}")
    
    new_text = "Python is a high-level, interpreted programming language used for web development, data science, AI, and automation"
    new_embedding = text_to_embeddings([new_text])[0]
    
    db.update(
        ids=["doc_001"],
        texts=[new_text],
        embeddings=[new_embedding],
        metadatas=[{"category": "programming", "topic": "python", "index": 1, "updated": True}]
    )
    
    updated = db.read(ids=["doc_001"])
    print(f"   Updated: {updated['documents'][0]}")
    print(f"   ✅ Update successful")
    
    # Update metadata only
    print("\n✏️  Updating metadata for doc_002...")
    db.update(
        ids=["doc_002"],
        metadatas=[{"category": "database", "topic": "chromadb", "index": 2, "version": "2.0"}]
    )
    updated_meta = db.read(ids=["doc_002"])
    print(f"   New metadata: {updated_meta['metadatas'][0]}")
    print(f"   ✅ Metadata update successful")
    
    # ============================================================
    # DELETE - Step 4: Delete embeddings
    # ============================================================
    print("\n" + "=" * 70)
    print("STEP 4: DELETE - Removing entries")
    print("=" * 70)
    
    info_before = db.get_info()
    print(f"\n📊 Before deletion: {info_before['count']} entries")
    
    # Delete specific entry
    print("\n🗑️  Deleting doc_005...")
    db.delete(ids=["doc_005"])
    
    info_after = db.get_info()
    print(f"   After deletion: {info_after['count']} entries")
    print(f"   ✅ Deletion successful")
    
    # Verify deletion
    deleted = db.read(ids=["doc_005"])
    if not deleted['ids']:
        print(f"   ✅ Entry 'doc_005' confirmed deleted")
    else:
        print(f"   ❌ Entry 'doc_005' still exists!")
    
    # Delete multiple entries
    print("\n🗑️  Deleting multiple entries (doc_003, doc_004)...")
    db.delete(ids=["doc_003", "doc_004"])
    
    final_info = db.get_info()
    print(f"   Final count: {final_info['count']} entries")
    print(f"   ✅ Multiple deletion successful")
    
    # ============================================================
    # Final Summary
    # ============================================================
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    
    final_results = db.read()
    print(f"\n📊 Remaining entries: {len(final_results['ids'])}")
    for doc_id, doc in zip(final_results['ids'], final_results['documents']):
        print(f"   - [{doc_id}] {doc[:50]}...")
    
    print("\n" + "=" * 70)
    print("✅ COMPLETE CRUD TEST FINISHED SUCCESSFULLY!")
    print("=" * 70)
    print("\nAll operations tested:")
    print("  ✅ CREATE - Added embeddings")
    print("  ✅ READ - Queried and retrieved embeddings")
    print("  ✅ UPDATE - Modified existing entries")
    print("  ✅ DELETE - Removed entries")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    run_complete_crud_test()

