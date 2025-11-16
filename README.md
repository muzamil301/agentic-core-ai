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

