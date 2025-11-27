"""
Read and query embeddings from ChromaDB
"""
import sys
from pathlib import Path
import numpy as np

# Add parent directories to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from db.chromadb_service import ChromaDBService
from utils import text_to_embeddings

# Configuration
COLLECTION_NAME = "payment_support"


def read_all_embeddings():
    """Read all embeddings from the collection"""
    print("=" * 60)
    print("Reading All Embeddings")
    print("=" * 60)
    
    db_service = ChromaDBService(collection_name=COLLECTION_NAME)
    
    # Get all entries
    results = db_service.read()
    
    print(f"\n📖 Found {len(results['ids'])} entries in collection '{COLLECTION_NAME}'")
    
    if not results['ids']:
        print("\n⚠️  Collection is empty. No entries found.")
        return
    
    print("\n" + "-" * 60)
    for i, (doc_id, doc, metadata) in enumerate(
        zip(results['ids'], results['documents'], results['metadatas']), 
        1
    ):
        print(f"\n{i}. ID: {doc_id}")
        print(f"   Text: {doc[:100]}{'...' if len(doc) > 100 else ''}")
        if metadata:
            print(f"   Metadata: {metadata}")
    
    print("\n" + "=" * 60)
    print("✅ Read operation completed!")
    print("=" * 60)


def read_by_ids(ids: list):
    """Read specific embeddings by their IDs"""
    print("=" * 60)
    print("Reading Embeddings by IDs")
    print("=" * 60)
    
    db_service = ChromaDBService(collection_name=COLLECTION_NAME)
    
    print(f"\n📖 Retrieving {len(ids)} entries by IDs: {ids}")
    
    results = db_service.read(ids=ids)
    
    if not results['ids']:
        print("\n⚠️  No entries found with the provided IDs.")
        return
    
    print(f"\n✅ Found {len(results['ids'])} entries")
    print("\n" + "-" * 60)
    
    for i, (doc_id, doc, metadata) in enumerate(
        zip(results['ids'], results['documents'], results['metadatas']), 
        1
    ):
        print(f"\n{i}. ID: {doc_id}")
        print(f"   Text: {doc}")
        if metadata:
            print(f"   Metadata: {metadata}")
    
    print("\n" + "=" * 60)
    print("✅ Read by IDs completed!")
    print("=" * 60)


def search_by_text(query: str, n_results: int = 5):
    """Search embeddings using text query (semantic search)"""
    print("=" * 60)
    print("Semantic Search by Text Query")
    print("=" * 60)
    
    db_service = ChromaDBService(collection_name=COLLECTION_NAME)
    
    print(f"\n🔍 Searching for: '{query}'")
    print(f"   Max results: {n_results}")
    
    results = db_service.read(
        query_texts=[query],
        n_results=n_results
    )
    
    if not results['ids'] or not results['ids'][0]:
        print("\n⚠️  No results found.")
        return
    
    print(f"\n✅ Found {len(results['ids'][0])} similar entries")
    print("\n" + "-" * 60)
    
    for i, (doc_id, doc, distance) in enumerate(
        zip(results['ids'][0], results['documents'][0], results['distances'][0]), 
        1
    ):
        print(f"\n{i}. ID: {doc_id}")
        print(f"   Text: {doc[:100]}{'...' if len(doc) > 100 else ''}")
        print(f"   Similarity Distance: {distance:.4f} (lower = more similar)")
    
    print("\n" + "=" * 60)
    print("✅ Search completed!")
    print("=" * 60)


def search_with_metadata_filter(query: str, filter_dict: dict, n_results: int = 5):
    """Search embeddings with metadata filter"""
    print("=" * 60)
    print("Search with Metadata Filter")
    print("=" * 60)
    
    db_service = ChromaDBService(collection_name=COLLECTION_NAME)
    
    print(f"\n🔍 Searching for: '{query}'")
    print(f"   Filter: {filter_dict}")
    print(f"   Max results: {n_results}")
    
    results = db_service.read(
        query_texts=[query],
        n_results=n_results,
        where=filter_dict
    )
    
    if not results['ids'] or not results['ids'][0]:
        print("\n⚠️  No results found matching the filter.")
        return
    
    print(f"\n✅ Found {len(results['ids'][0])} entries matching filter")
    print("\n" + "-" * 60)
    
    for i, (doc_id, doc, metadata, distance) in enumerate(
        zip(
            results['ids'][0], 
            results['documents'][0], 
            results['metadatas'][0],
            results['distances'][0]
        ), 
        1
    ):
        print(f"\n{i}. ID: {doc_id}")
        print(f"   Text: {doc[:100]}{'...' if len(doc) > 100 else ''}")
        print(f"   Metadata: {metadata}")
        print(f"   Distance: {distance:.4f}")
    
    print("\n" + "=" * 60)
    print("✅ Filtered search completed!")
    print("=" * 60)


def show_raw_embeddings_all():
    """Show raw embedding vectors for all entries"""
    print("=" * 60)
    print("Raw Embedding Vectors - All Entries")
    print("=" * 60)
    
    db_service = ChromaDBService(collection_name=COLLECTION_NAME)
    
    # Get all entries with embeddings
    results = db_service.read()
    
    print(f"\n📖 Found {len(results['ids'])} entries in collection '{COLLECTION_NAME}'")
    
    if not results['ids']:
        print("\n⚠️  Collection is empty. No entries found.")
        return
    
    # Check if embeddings exist and are not empty
    if 'embeddings' not in results:
        print("\n⚠️  No embedding vectors found in results.")
        print("   Note: Embeddings key not found in results")
        print(f"   Available keys: {list(results.keys())}")
        return
    
    embeddings_list = results['embeddings']
    if embeddings_list is None:
        print("\n⚠️  No embedding vectors found in results.")
        print("   Note: Embeddings list is None")
        return
    
    if isinstance(embeddings_list, list) and len(embeddings_list) == 0:
        print("\n⚠️  No embedding vectors found in results.")
        print("   Note: Embeddings list is empty")
        return
    
    print("\n" + "-" * 60)
    
    for i, (doc_id, doc, embedding) in enumerate(
        zip(results['ids'], results['documents'], results['embeddings']), 
        1
    ):
        emb_array = np.array(embedding)
        
        print(f"\n{i}. ID: {doc_id}")
        print(f"   Text: {doc[:60]}{'...' if len(doc) > 60 else ''}")
        print(f"\n   Embedding Vector:")
        print(f"      Dimension: {emb_array.shape[0]}")
        print(f"      Shape: {emb_array.shape}")
        print(f"      Data Type: {emb_array.dtype}")
        print(f"      Min Value: {emb_array.min():.6f}")
        print(f"      Max Value: {emb_array.max():.6f}")
        print(f"      Mean: {emb_array.mean():.6f}")
        print(f"      Std Dev: {emb_array.std():.6f}")
        
        # Show first 10 values
        print(f"\n      First 10 values:")
        print(f"      {emb_array[:10]}")
        
        # Show last 10 values
        print(f"\n      Last 10 values:")
        print(f"      {emb_array[-10:]}")
        
        # Option to show full vector
        show_full = input(f"\n   Show full vector for this entry? (y/n, default n): ").strip().lower()
        if show_full == 'y':
            print(f"\n      Full Vector ({len(emb_array)} values):")
            # Print in rows of 10 for readability
            for j in range(0, len(emb_array), 10):
                end_idx = min(j + 10, len(emb_array))
                values = emb_array[j:end_idx]
                print(f"      [{j:4d}:{end_idx:4d}] {values}")
        
        print("\n" + "-" * 60)
    
    print("\n" + "=" * 60)
    print("✅ Raw embeddings display completed!")
    print("=" * 60)


def show_raw_embeddings_by_ids(ids: list):
    """Show raw embedding vectors for specific IDs"""
    print("=" * 60)
    print("Raw Embedding Vectors - By IDs")
    print("=" * 60)
    
    db_service = ChromaDBService(collection_name=COLLECTION_NAME)
    
    print(f"\n📖 Retrieving {len(ids)} entries by IDs: {ids}")
    
    results = db_service.read(ids=ids)
    
    if not results['ids']:
        print("\n⚠️  No entries found with the provided IDs.")
        return
    
    # Check if embeddings exist and are not empty
    if 'embeddings' not in results:
        print("\n⚠️  No embedding vectors found.")
        return
    
    embeddings_list = results['embeddings']
    if embeddings_list is None or len(embeddings_list) == 0:
        print("\n⚠️  No embedding vectors found.")
        return
    
    print(f"\n✅ Found {len(results['ids'])} entries")
    print("\n" + "-" * 60)
    
    for i, (doc_id, doc, embedding) in enumerate(
        zip(results['ids'], results['documents'], results['embeddings']), 
        1
    ):
        emb_array = np.array(embedding)
        
        print(f"\n{i}. ID: {doc_id}")
        print(f"   Text: {doc}")
        print(f"\n   Embedding Vector Statistics:")
        print(f"      Dimension: {emb_array.shape[0]}")
        print(f"      Min: {emb_array.min():.6f}")
        print(f"      Max: {emb_array.max():.6f}")
        print(f"      Mean: {emb_array.mean():.6f}")
        print(f"      Std: {emb_array.std():.6f}")
        
        print(f"\n   Full Vector ({len(emb_array)} values):")
        # Print in rows of 10
        for j in range(0, len(emb_array), 10):
            end_idx = min(j + 10, len(emb_array))
            values = emb_array[j:end_idx]
            print(f"      [{j:4d}:{end_idx:4d}] {values}")
        
        print("\n" + "-" * 60)
    
    print("\n" + "=" * 60)
    print("✅ Raw embeddings display completed!")
    print("=" * 60)


def show_raw_embeddings_from_search(query: str, n_results: int = 5):
    """Show raw embedding vectors from search results"""
    print("=" * 60)
    print("Raw Embedding Vectors - From Search")
    print("=" * 60)
    
    db_service = ChromaDBService(collection_name=COLLECTION_NAME)
    
    print(f"\n🔍 Searching for: '{query}'")
    print(f"   Max results: {n_results}")
    
    results = db_service.read(
        query_texts=[query],
        n_results=n_results
    )
    
    if not results['ids'] or not results['ids'][0]:
        print("\n⚠️  No results found.")
        return
    
    # Check if embeddings exist and are not empty
    if 'embeddings' not in results:
        print("\n⚠️  No embedding vectors found in results.")
        return
    
    embeddings_list = results['embeddings']
    if embeddings_list is None:
        print("\n⚠️  No embedding vectors found in results.")
        return
    
    if isinstance(embeddings_list, list) and len(embeddings_list) == 0:
        print("\n⚠️  No embedding vectors found in results.")
        return
    
    if len(embeddings_list) > 0:
        first_embedding = embeddings_list[0]
        if first_embedding is None or (isinstance(first_embedding, list) and len(first_embedding) == 0):
            print("\n⚠️  No embedding vectors found in results.")
            return
    
    print(f"\n✅ Found {len(results['ids'][0])} similar entries")
    print("\n" + "-" * 60)
    
    for i, (doc_id, doc, embedding, distance) in enumerate(
        zip(
            results['ids'][0], 
            results['documents'][0], 
            results['embeddings'][0],
            results['distances'][0]
        ), 
        1
    ):
        emb_array = np.array(embedding)
        
        print(f"\n{i}. ID: {doc_id}")
        print(f"   Text: {doc[:60]}{'...' if len(doc) > 60 else ''}")
        print(f"   Similarity Distance: {distance:.4f}")
        print(f"\n   Embedding Vector:")
        print(f"      Dimension: {emb_array.shape[0]}")
        print(f"      Min: {emb_array.min():.6f}")
        print(f"      Max: {emb_array.max():.6f}")
        print(f"      Mean: {emb_array.mean():.6f}")
        
        # Show first 20 values
        print(f"\n      First 20 values:")
        print(f"      {emb_array[:20]}")
        
        # Ask if user wants full vector
        show_full = input(f"\n   Show full vector? (y/n, default n): ").strip().lower()
        if show_full == 'y':
            print(f"\n      Full Vector ({len(emb_array)} values):")
            for j in range(0, len(emb_array), 10):
                end_idx = min(j + 10, len(emb_array))
                values = emb_array[j:end_idx]
                print(f"      [{j:4d}:{end_idx:4d}] {values}")
        
        print("\n" + "-" * 60)
    
    print("\n" + "=" * 60)
    print("✅ Raw embeddings display completed!")
    print("=" * 60)


def main():
    """Main function with interactive menu"""
    print("=" * 60)
    print("Read Embeddings - ChromaDB")
    print("=" * 60)
    
    print("\nSelect an option:")
    print("1. Read all embeddings")
    print("2. Read by specific IDs")
    print("3. Search by text query")
    print("4. Search with metadata filter")
    print("5. Run all read operations")
    print("6. Show raw embedding vectors (all entries)")
    print("7. Show raw embedding vectors (by IDs)")
    print("8. Show raw embedding vectors (from search)")
    
    choice = input("\nEnter your choice (1-8): ").strip()
    
    if choice == "1":
        read_all_embeddings()
    
    elif choice == "2":
        ids_input = input("Enter IDs (comma-separated): ").strip()
        ids = [id.strip() for id in ids_input.split(",")]
        read_by_ids(ids)
    
    elif choice == "3":
        query = input("Enter search query: ").strip()
        n_results = input("Number of results (default 5): ").strip()
        n_results = int(n_results) if n_results else 5
        search_by_text(query, n_results)
    
    elif choice == "4":
        query = input("Enter search query: ").strip()
        filter_key = input("Enter metadata filter key (e.g., 'category'): ").strip()
        filter_value = input(f"Enter value for '{filter_key}': ").strip()
        n_results = input("Number of results (default 5): ").strip()
        n_results = int(n_results) if n_results else 5
        
        filter_dict = {filter_key: filter_value}
        search_with_metadata_filter(query, filter_dict, n_results)
    
    elif choice == "5":
        read_all_embeddings()
        print("\n")
        search_by_text("transaction limit", n_results=3)
        print("\n")
        search_by_text("card", n_results=3)
    
    elif choice == "6":
        show_raw_embeddings_all()
    
    elif choice == "7":
        ids_input = input("Enter IDs (comma-separated): ").strip()
        ids = [id.strip() for id in ids_input.split(",")]
        show_raw_embeddings_by_ids(ids)
    
    elif choice == "8":
        query = input("Enter search query: ").strip()
        n_results = input("Number of results (default 5): ").strip()
        n_results = int(n_results) if n_results else 5
        show_raw_embeddings_from_search(query, n_results)
    
    else:
        print("❌ Invalid choice. Please run the script again.")


if __name__ == "__main__":
    main()

