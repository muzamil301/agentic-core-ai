# Embeddings Project

A Python project for generating embeddings from text data and storing them in ChromaDB for semantic search and retrieval.

## Overview

This project provides a complete solution for:
- Generating embeddings using Ollama API
- Storing embeddings in ChromaDB
- Performing CRUD operations on embeddings
- Semantic search and retrieval

## Project Structure

```
embeddings-py/
├── db/                          # Database layer
│   ├── __init__.py
│   └── chromadb_service.py      # ChromaDB service with CRUD operations
├── mock-data/                   # Data files
│   └── payment_support_data.json
├── config.py                    # Configuration constants
├── utils.py                     # Utility functions for embeddings
├── payment_support_embeddings.py # Main script example
├── get_embeddings.py            # Simple embedding test script
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Prerequisites

1. **Python 3.8+**
2. **Ollama** running locally with the `all-minilm` model
   - Install Ollama: https://ollama.ai
   - Pull the model: `ollama pull all-minilm`

## Installation

1. Clone or navigate to the project directory:
```bash
cd embeddings-py
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure Ollama is running:
```bash
# Start Ollama service should be running
# Check with: curl http://localhost:11434/api/tags
```

## Quick Start

### Generate and Store Embeddings from JSON

Run the main script to process payment support data:

```bash
python payment_support_embeddings.py
```

This will:
1. Load data from `mock-data/payment_support_data.json`
2. Generate embeddings using Ollama API
3. Store embeddings in ChromaDB collection named "payment_support"

### Test Embedding Generation

Test the embedding generation with simple text:

```bash
python get_embeddings.py
```

## Usage Guide

### 1. Basic Setup

```python
from db.chromadb_service import ChromaDBService
from utils import text_to_embeddings, json_to_embeddings

# Initialize service with a collection
db_service = ChromaDBService(collection_name="my_collection")
```

### 2. Create (Write) Embeddings

#### From Text Strings

```python
# Generate embeddings from text
texts = [
    "What is my daily transaction limit?",
    "How do I block my card?",
    "How long do international transfers take?"
]

# Generate embeddings using Ollama
embeddings = text_to_embeddings(texts)

# Store in ChromaDB
ids = db_service.create(
    texts=texts,
    embeddings=embeddings,
    ids=["id1", "id2", "id3"],  # Optional: auto-generated if None
    metadatas=[                  # Optional: metadata for each entry
        {"category": "limits"},
        {"category": "card"},
        {"category": "transfers"}
    ]
)
print(f"Created embeddings with IDs: {ids}")
```

#### From JSON File

```python
# Load JSON and convert to embeddings
texts, embeddings, ids, metadatas = json_to_embeddings(
    json_file_path="mock-data/payment_support_data.json",
    combine_fields=["question", "answer"],  # Combine multiple fields
    id_field="id",                          # Field to use as ID
    metadata_fields=["category", "keywords"] # Fields to include as metadata
)

# Store in ChromaDB
created_ids = db_service.create(
    texts=texts,
    embeddings=embeddings,
    ids=ids,
    metadatas=metadatas
)
```

### 3. Read (Query) Embeddings

#### Get All Embeddings

```python
# Get all entries in the collection
results = db_service.read()

print(f"Total entries: {len(results['ids'])}")
for i, doc in enumerate(results['documents']):
    print(f"{i+1}. {doc}")
```

#### Search by Text Query

```python
# Semantic search using text queries
results = db_service.read(
    query_texts=["How do I block my card?"],
    n_results=3  # Number of results to return
)

# Results contain:
# - ids: List of result IDs
# - documents: List of text documents
# - embeddings: List of embedding vectors
# - distances: Similarity distances (lower = more similar)
# - metadatas: List of metadata dictionaries

for i, (doc, distance) in enumerate(zip(results['documents'], results['distances'][0])):
    print(f"{i+1}. {doc} (distance: {distance:.4f})")
```

#### Search by Embedding Vectors

```python
# Search using pre-computed embeddings
query_embeddings = text_to_embeddings(["transaction limit"])

results = db_service.read(
    query_embeddings=query_embeddings,
    n_results=5
)
```

#### Get by Specific IDs

```python
# Retrieve specific entries by ID
results = db_service.read(ids=["support_001", "support_002"])

for doc in results['documents']:
    print(doc)
```

#### Filter by Metadata

```python
# Search with metadata filters
results = db_service.read(
    query_texts=["card"],
    n_results=10,
    where={"category": "card_management"}  # Filter by metadata
)
```

### 4. Update Embeddings

```python
# Update existing embeddings
db_service.update(
    ids=["support_001"],
    texts=["Updated question and answer text"],
    embeddings=[new_embedding_vector],  # New embedding vector
    metadatas=[{"category": "updated_category"}]
)

# Update only specific fields (others remain unchanged)
db_service.update(
    ids=["support_001"],
    texts=["Only updating the text"],
    # embeddings and metadatas will be preserved from existing entry
)
```

### 5. Delete Embeddings

```python
# Delete specific entries
db_service.delete(ids=["support_001", "support_002"])

# Delete all entries in collection
db_service.delete()  # or db_service.clear_collection()
```

### 6. Get Collection Information

```python
# Get collection statistics
info = db_service.get_info()

print(f"Collection: {info['collection_name']}")
print(f"Total entries: {info['count']}")
print(f"Metadata: {info['metadata']}")
```

### 7. Collection Management

```python
# List all collections
collections = db_service.list_collections()
print(f"Available collections: {collections}")

# Switch to a different collection
db_service.set_collection("another_collection")

# Delete a collection
db_service.delete_collection("old_collection")
```

## Complete Example

```python
from db.chromadb_service import ChromaDBService
from utils import text_to_embeddings

# Initialize service
db = ChromaDBService(collection_name="example")

# 1. Create embeddings
texts = ["Python is a programming language", "ChromaDB stores vectors"]
embeddings = text_to_embeddings(texts)
ids = db.create(texts=texts, embeddings=embeddings)

# 2. Read/search embeddings
results = db.read(query_texts=["programming"], n_results=2)
print(f"Found {len(results['documents'])} results")

# 3. Update an embedding
new_text = "Python is a high-level programming language"
new_embedding = text_to_embeddings([new_text])[0]
db.update(ids=[ids[0]], texts=[new_text], embeddings=[new_embedding])

# 4. Get collection info
info = db.get_info()
print(f"Collection has {info['count']} entries")

# 5. Delete an entry
db.delete(ids=[ids[1]])

# 6. Clear all entries
db.clear_collection()
```

## Configuration

Edit `config.py` to customize:

```python
# Ollama API Configuration
OLLAMA_API_URL = "http://localhost:11434/api/embed"
EMBEDDING_MODEL = "all-minilm"
OLLAMA_TIMEOUT = 60

# ChromaDB Configuration
CHROMADB_PERSIST_DIRECTORY = "./chroma_db"
DEFAULT_COLLECTION_NAME = "embeddings"
```

## Database Functions Reference

### ChromaDBService Methods

| Method | Description | Parameters |
|--------|-------------|------------|
| `create()` | Write embeddings to ChromaDB | `texts`, `embeddings`, `ids`, `metadatas` |
| `read()` | Query/retrieve embeddings | `query_texts`, `query_embeddings`, `ids`, `n_results`, `where` |
| `update()` | Update existing embeddings | `ids`, `texts`, `embeddings`, `metadatas` |
| `delete()` | Delete embeddings | `ids` (optional, deletes all if None) |
| `get_info()` | Get collection statistics | None |
| `clear_collection()` | Clear all entries | None |
| `set_collection()` | Switch active collection | `collection_name`, `create_if_not_exists` |
| `list_collections()` | List all collections | None |
| `delete_collection()` | Delete a collection | `collection_name` |

## Utility Functions

### `text_to_embeddings(texts, model, api_url)`
Converts a list of text strings to embeddings using Ollama API.

### `json_to_embeddings(json_file_path, text_field, id_field, metadata_fields, combine_fields)`
Loads JSON file and converts to embeddings with metadata extraction.

### `get_embedding_info(embeddings)`
Returns statistics about generated embeddings (count, dimension, sample values).

## Troubleshooting

### Ollama Connection Error
- Ensure Ollama is running: `ollama serve`
- Check if model is available: `ollama list`
- Pull the model if missing: `ollama pull all-minilm`

### ChromaDB Errors
- Check if `chroma_db` directory exists and is writable
- Verify collection name is valid (no special characters)

### Import Errors
- Ensure you're running from the project root directory
- Check that all dependencies are installed: `pip install -r requirements.txt`

## License

This project is for educational and development purposes.

