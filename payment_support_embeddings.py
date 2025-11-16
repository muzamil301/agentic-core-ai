from db.chromadb_service import ChromaDBService
from utils import json_to_embeddings, get_embedding_info

# JSON file path
JSON_FILE_PATH = "mock-data/payment_support_data.json"


def main():
    """
    Main function to process payment support data from JSON and store embeddings.
    """
    print("=" * 60)
    print("Payment Support System - Embedding Generation")
    print("=" * 60)
    
    # Load JSON and convert to embeddings using utility function
    print(f"\n📂 Loading data from {JSON_FILE_PATH}...")
    texts, embeddings, ids, metadatas = json_to_embeddings(
        json_file_path=JSON_FILE_PATH,
        combine_fields=["question", "answer"],  # Combine question and answer
        id_field="id",
        metadata_fields=["category", "keywords"]
    )
    
    # Display the data being processed
    print(f"\n📋 Processing {len(texts)} support entries:")
    for i, (text, metadata) in enumerate(zip(texts, metadatas), 1):
        print(f"\n{i}. {metadata.get('category', 'N/A').upper()}")
        print(f"   {text[:100]}...")
    
    # Display embedding info
    embedding_info = get_embedding_info(embeddings)
    print(f"\n📊 Embedding Information:")
    print(f"   Count: {embedding_info['count']}")
    print(f"   Dimension: {embedding_info['dimension']}")
    
    # Store embeddings in ChromaDB using service
    print("\n💾 Storing embeddings in ChromaDB...")
    db_service = ChromaDBService(collection_name="payment_support")
    created_ids = db_service.create(
        texts=texts,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )
    
    print(f"✅ Successfully stored {len(created_ids)} embeddings in ChromaDB")
    
    # Display collection info
    info = db_service.get_info()
    print(f"\n📊 Collection Info:")
    print(f"   Collection: {info['collection_name']}")
    print(f"   Total entries: {info['count']}")
    
    print("\n" + "=" * 60)
    print("✅ Process completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()

