"""
Delete embeddings from ChromaDB
"""
import sys
from pathlib import Path

# Add parent directories to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from db.chromadb_service import ChromaDBService

# Configuration
COLLECTION_NAME = "payment_support"


def delete_by_ids(ids: list):
    """Delete specific embeddings by their IDs"""
    print("=" * 60)
    print("Delete Embeddings by IDs")
    print("=" * 60)
    
    db_service = ChromaDBService(collection_name=COLLECTION_NAME)
    
    # Check current state
    info_before = db_service.get_info()
    print(f"\n📊 Collection state before deletion:")
    print(f"   Collection: {info_before['collection_name']}")
    print(f"   Total entries: {info_before['count']}")
    
    # Verify IDs exist
    print(f"\n🔍 Verifying IDs exist...")
    existing = db_service.read(ids=ids)
    
    if not existing['ids']:
        print(f"\n⚠️  None of the provided IDs exist in the collection.")
        print(f"   Requested IDs: {ids}")
        return
    
    found_ids = existing['ids']
    missing_ids = set(ids) - set(found_ids)
    
    if missing_ids:
        print(f"\n⚠️  Some IDs not found: {missing_ids}")
        print(f"   Will delete only existing IDs: {found_ids}")
    
    print(f"\n🗑️  Deleting {len(found_ids)} entry/entries...")
    
    # Delete the entries
    db_service.delete(ids=list(found_ids))
    
    # Verify deletion
    print("\n✅ Deletion completed. Verifying...")
    info_after = db_service.get_info()
    print(f"\n📊 Collection state after deletion:")
    print(f"   Total entries: {info_after['count']}")
    print(f"   Deleted: {info_before['count'] - info_after['count']} entry/entries")
    
    # Try to read deleted entries
    deleted_check = db_service.read(ids=list(found_ids))
    if not deleted_check['ids']:
        print(f"\n✅ Successfully deleted IDs: {found_ids}")
    else:
        print(f"\n⚠️  Warning: Some entries may still exist: {deleted_check['ids']}")
    
    print("\n" + "=" * 60)
    print("✅ Delete operation completed!")
    print("=" * 60)


def delete_all():
    """Delete all embeddings from the collection"""
    print("=" * 60)
    print("Delete All Embeddings")
    print("=" * 60)
    
    db_service = ChromaDBService(collection_name=COLLECTION_NAME)
    
    # Check current state
    info_before = db_service.get_info()
    print(f"\n📊 Collection state before deletion:")
    print(f"   Collection: {info_before['collection_name']}")
    print(f"   Total entries: {info_before['count']}")
    
    if info_before['count'] == 0:
        print("\n⚠️  Collection is already empty. Nothing to delete.")
        return
    
    # Confirm deletion
    print(f"\n⚠️  WARNING: This will delete ALL {info_before['count']} entries from the collection!")
    confirm = input("Are you sure you want to continue? (yes/no): ").strip().lower()
    
    if confirm not in ['yes', 'y']:
        print("\n❌ Deletion cancelled.")
        return
    
    print(f"\n🗑️  Deleting all entries...")
    db_service.clear_collection()
    
    # Verify deletion
    print("\n✅ Deletion completed. Verifying...")
    info_after = db_service.get_info()
    print(f"\n📊 Collection state after deletion:")
    print(f"   Total entries: {info_after['count']}")
    
    if info_after['count'] == 0:
        print(f"\n✅ Successfully deleted all {info_before['count']} entries")
    else:
        print(f"\n⚠️  Warning: Collection still has {info_after['count']} entries")
    
    print("\n" + "=" * 60)
    print("✅ Delete all operation completed!")
    print("=" * 60)


def show_collection_contents():
    """Show current collection contents before deletion"""
    print("=" * 60)
    print("Current Collection Contents")
    print("=" * 60)
    
    db_service = ChromaDBService(collection_name=COLLECTION_NAME)
    
    results = db_service.read()
    
    if not results['ids']:
        print("\n⚠️  Collection is empty.")
        return
    
    print(f"\n📖 Found {len(results['ids'])} entries:")
    print("\n" + "-" * 60)
    
    for i, (doc_id, doc) in enumerate(zip(results['ids'], results['documents']), 1):
        print(f"\n{i}. ID: {doc_id}")
        print(f"   Text: {doc[:80]}{'...' if len(doc) > 80 else ''}")
    
    print("\n" + "=" * 60)


def main():
    """Main function with interactive menu"""
    print("=" * 60)
    print("Delete Embeddings - ChromaDB")
    print("=" * 60)
    
    # Show current contents first
    show_collection_contents()
    
    print("\n\nSelect an option:")
    print("1. Delete by specific IDs")
    print("2. Delete all embeddings")
    print("3. Show collection contents only")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        ids_input = input("Enter IDs to delete (comma-separated): ").strip()
        ids = [id.strip() for id in ids_input.split(",") if id.strip()]
        
        if not ids:
            print("❌ No IDs provided.")
            return
        
        delete_by_ids(ids)
    
    elif choice == "2":
        delete_all()
    
    elif choice == "3":
        # Already shown above, just exit
        pass
    
    else:
        print("❌ Invalid choice. Please run the script again.")


if __name__ == "__main__":
    main()

