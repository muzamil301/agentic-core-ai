"""
Get information about ChromaDB collections
"""
import sys
from pathlib import Path

# Add parent directories to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from db.chromadb_service import ChromaDBService

# Configuration
COLLECTION_NAME = "payment_support"


def get_collection_info():
    """Get detailed information about a collection"""
    print("=" * 60)
    print("Collection Information")
    print("=" * 60)
    
    db_service = ChromaDBService(collection_name=COLLECTION_NAME)
    
    # Get collection info
    info = db_service.get_info()
    
    print(f"\n📊 Collection Details:")
    print(f"   Name: {info['collection_name']}")
    print(f"   Total Entries: {info['count']}")
    print(f"   Metadata: {info['metadata']}")
    
    # Get all entries for detailed view
    if info['count'] > 0:
        results = db_service.read()
        
        print(f"\n📖 Entry Details:")
        print("-" * 60)
        
        for i, (doc_id, doc, metadata) in enumerate(
            zip(results['ids'], results['documents'], results['metadatas']), 
            1
        ):
            print(f"\n{i}. ID: {doc_id}")
            print(f"   Text Preview: {doc[:60]}{'...' if len(doc) > 60 else ''}")
            if metadata:
                print(f"   Metadata: {metadata}")
    else:
        print("\n⚠️  Collection is empty.")
    
    print("\n" + "=" * 60)
    print("✅ Info retrieval completed!")
    print("=" * 60)


def list_all_collections():
    """List all collections in the database"""
    print("=" * 60)
    print("All Collections in Database")
    print("=" * 60)
    
    db_service = ChromaDBService(collection_name=COLLECTION_NAME, create_collection=False)
    
    collections = db_service.list_collections()
    
    if not collections:
        print("\n⚠️  No collections found in the database.")
        return
    
    print(f"\n📚 Found {len(collections)} collection(s):")
    print("-" * 60)
    
    for i, collection_name in enumerate(collections, 1):
        # Get info for each collection
        temp_service = ChromaDBService(collection_name=collection_name)
        info = temp_service.get_info()
        
        print(f"\n{i}. Collection: {collection_name}")
        print(f"   Entries: {info['count']}")
        print(f"   Metadata: {info['metadata']}")
    
    print("\n" + "=" * 60)
    print("✅ Collections listing completed!")
    print("=" * 60)


def get_statistics():
    """Get statistics about the collection"""
    print("=" * 60)
    print("Collection Statistics")
    print("=" * 60)
    
    db_service = ChromaDBService(collection_name=COLLECTION_NAME)
    
    info = db_service.get_info()
    results = db_service.read()
    
    print(f"\n📊 Statistics:")
    print(f"   Collection Name: {info['collection_name']}")
    print(f"   Total Entries: {info['count']}")
    
    if info['count'] > 0:
        # Calculate text statistics
        texts = results['documents']
        total_chars = sum(len(text) for text in texts)
        avg_chars = total_chars / len(texts) if texts else 0
        
        # Metadata statistics
        metadatas = results['metadatas']
        if metadatas:
            # Count categories if they exist
            categories = {}
            for meta in metadatas:
                if 'category' in meta:
                    cat = meta['category']
                    categories[cat] = categories.get(cat, 0) + 1
            
            print(f"\n   Text Statistics:")
            print(f"   - Total Characters: {total_chars:,}")
            print(f"   - Average Characters per Entry: {avg_chars:.1f}")
            print(f"   - Longest Entry: {max(len(t) for t in texts)} chars")
            print(f"   - Shortest Entry: {min(len(t) for t in texts)} chars")
            
            if categories:
                print(f"\n   Category Distribution:")
                for cat, count in categories.items():
                    print(f"   - {cat}: {count} entry/entries")
    
    print("\n" + "=" * 60)
    print("✅ Statistics retrieval completed!")
    print("=" * 60)


def main():
    """Main function with interactive menu"""
    print("=" * 60)
    print("Get Collection Information - ChromaDB")
    print("=" * 60)
    
    print("\nSelect an option:")
    print("1. Get collection info (default collection)")
    print("2. List all collections")
    print("3. Get detailed statistics")
    print("4. Show all information")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        get_collection_info()
    
    elif choice == "2":
        list_all_collections()
    
    elif choice == "3":
        get_statistics()
    
    elif choice == "4":
        get_collection_info()
        print("\n")
        get_statistics()
        print("\n")
        list_all_collections()
    
    else:
        print("❌ Invalid choice. Please run the script again.")


if __name__ == "__main__":
    main()

