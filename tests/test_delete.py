"""
Test script for DELETE operation - Deleting embeddings from ChromaDB
"""
from db.chromadb_service import ChromaDBService
from utils import text_to_embeddings

def test_delete_specific_entry():
    """Test deleting a specific entry by ID"""
    print("=" * 60)
    print("Testing DELETE Operation - Specific Entry")
    print("=" * 60)
    
    db = ChromaDBService(collection_name="test_collection")
    
    # First, check what we have
    print("\n📖 Current collection state:")
    info_before = db.get_info()
    print(f"   Total entries: {info_before['count']}")
    
    # Read all to see what exists
    all_entries = db.read()
    if all_entries['ids']:
        print(f"\n   Available IDs: {all_entries['ids']}")
    else:
        print("\n❌ No entries found. Run test_create.py first!")
        return
    
    # Delete a specific entry
    target_id = all_entries['ids'][0]  # Delete first entry
    print(f"\n🗑️  Deleting entry with ID: {target_id}")
    
    db.delete(ids=[target_id])
    
    # Verify deletion
    print("\n✅ Deletion completed. Verifying...")
    info_after = db.get_info()
    print(f"   Total entries after deletion: {info_after['count']}")
    
    # Try to read the deleted entry
    deleted_entry = db.read(ids=[target_id])
    if not deleted_entry['ids']:
        print(f"   ✅ Entry '{target_id}' successfully deleted")
    else:
        print(f"   ❌ Entry '{target_id}' still exists!")
    
    print("\n" + "=" * 60)
    print("✅ DELETE SPECIFIC test completed!")
    print("=" * 60)

def test_delete_multiple_entries():
    """Test deleting multiple entries"""
    print("\n" + "=" * 60)
    print("Testing DELETE Operation - Multiple Entries")
    print("=" * 60)
    
    db = ChromaDBService(collection_name="test_collection")
    
    # First, add some test entries if needed
    print("\n📝 Adding test entries for deletion...")
    texts = [
        "Test entry 1 for deletion",
        "Test entry 2 for deletion",
        "Test entry 3 for deletion"
    ]
    embeddings = text_to_embeddings(texts)
    test_ids = ["delete_test_1", "delete_test_2", "delete_test_3"]
    
    db.create(
        texts=texts,
        embeddings=embeddings,
        ids=test_ids
    )
    
    print(f"   Created {len(test_ids)} test entries")
    
    # Check before deletion
    info_before = db.get_info()
    print(f"\n📊 Before deletion: {info_before['count']} entries")
    
    # Delete multiple entries
    print(f"\n🗑️  Deleting {len(test_ids)} entries...")
    db.delete(ids=test_ids)
    
    # Verify deletion
    print("\n✅ Deletion completed. Verifying...")
    info_after = db.get_info()
    print(f"   After deletion: {info_after['count']} entries")
    print(f"   Deleted: {info_before['count'] - info_after['count']} entries")
    
    # Verify entries are gone
    deleted_entries = db.read(ids=test_ids)
    if not deleted_entries['ids']:
        print(f"   ✅ All {len(test_ids)} entries successfully deleted")
    else:
        print(f"   ⚠️  Some entries still exist: {deleted_entries['ids']}")
    
    print("\n" + "=" * 60)
    print("✅ DELETE MULTIPLE test completed!")
    print("=" * 60)

def test_clear_collection():
    """Test clearing all entries from collection"""
    print("\n" + "=" * 60)
    print("Testing DELETE Operation - Clear Collection")
    print("=" * 60)
    
    db = ChromaDBService(collection_name="test_collection")
    
    # Check before clearing
    print("\n📊 Collection state before clearing:")
    info_before = db.get_info()
    print(f"   Total entries: {info_before['count']}")
    
    if info_before['count'] == 0:
        print("\n⚠️  Collection is already empty. Adding test entries...")
        texts = ["Test entry 1", "Test entry 2"]
        embeddings = text_to_embeddings(texts)
        db.create(texts=texts, embeddings=embeddings)
        info_before = db.get_info()
        print(f"   Added {info_before['count']} test entries")
    
    # Clear all entries
    print(f"\n🗑️  Clearing all {info_before['count']} entries from collection...")
    db.clear_collection()
    
    # Verify clearing
    print("\n✅ Clearing completed. Verifying...")
    info_after = db.get_info()
    print(f"   Total entries after clearing: {info_after['count']}")
    
    if info_after['count'] == 0:
        print("   ✅ Collection successfully cleared")
    else:
        print(f"   ❌ Collection still has {info_after['count']} entries!")
    
    print("\n" + "=" * 60)
    print("✅ CLEAR COLLECTION test completed!")
    print("=" * 60)

def test_delete_nonexistent_entry():
    """Test deleting an entry that doesn't exist (should not error)"""
    print("\n" + "=" * 60)
    print("Testing DELETE Operation - Non-existent Entry")
    print("=" * 60)
    
    db = ChromaDBService(collection_name="test_collection")
    
    nonexistent_id = "nonexistent_entry_12345"
    
    print(f"\n🗑️  Attempting to delete non-existent entry: {nonexistent_id}")
    
    try:
        db.delete(ids=[nonexistent_id])
        print("   ✅ Delete operation completed without error")
        print("   (ChromaDB handles non-existent IDs gracefully)")
    except Exception as e:
        print(f"   ⚠️  Error occurred: {e}")
    
    print("\n" + "=" * 60)
    print("✅ DELETE NON-EXISTENT test completed!")
    print("=" * 60)

if __name__ == "__main__":
    print("\n⚠️  Make sure you've run test_create.py first to populate the database!\n")
    
    test_delete_specific_entry()
    test_delete_multiple_entries()
    test_delete_nonexistent_entry()
    test_clear_collection()
    
    print("\n" + "=" * 60)
    print("✅ All DELETE tests completed!")
    print("=" * 60)
    print("\n💡 Note: Collection has been cleared. Run test_create.py to repopulate.")

