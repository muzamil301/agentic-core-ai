# Embeddings Management

This module provides tools and scripts for managing embeddings in ChromaDB. It handles the complete lifecycle of embeddings: Create, Read, Update, Delete (CRUD) operations.

## Directory Structure

```
embeddings-management/
├── __init__.py                     # Package initialization
├── README.md                       # This file
│
├── scripts/                        # Production scripts
│   ├── __init__.py
│   ├── payment_support_embeddings.py  # Create embeddings from JSON
│   ├── read_embeddings.py             # Read/query embeddings
│   ├── delete_embeddings.py           # Delete embeddings
│   └── get_info.py                    # Get collection info
│
├── examples/                       # Example and test scripts
│   ├── __init__.py
│   ├── get_embeddings.py              # Simple embedding example
│   └── test_complete_crud.py          # Complete CRUD test
│
└── tests/                          # Unit tests
    ├── __init__.py
    ├── test_create.py                 # Test CREATE operations
    ├── test_read.py                   # Test READ operations
    ├── test_update.py                 # Test UPDATE operations
    ├── test_delete.py                 # Test DELETE operations
    └── test_complete_crud.py          # Complete CRUD test
```

## Purpose

### Scripts (`scripts/`)
Production-ready scripts for managing embeddings:

- **Create**: Generate embeddings from data sources (JSON, CSV, etc.)
- **Read**: Query and inspect existing embeddings
- **Update**: Modify existing embeddings (metadata, content)
- **Delete**: Remove embeddings from collections
- **Info**: Get collection statistics and metadata

### Examples (`examples/`)
Learning and development scripts:

- Simple examples for understanding how embeddings work
- Complete CRUD workflow demonstrations
- Testing different scenarios

### Tests (`tests/`)
Unit tests for validating CRUD operations:

- Individual operation tests
- Integration tests
- Error handling tests

## Usage

### 1. Create Embeddings from Data

```bash
# From project root
python embeddings-management/scripts/payment_support_embeddings.py
```

This script:
- Loads data from `mock-data/payment_support_data.json`
- Generates embeddings using Ollama
- Stores embeddings in ChromaDB collection "payment_support"

### 2. Read/Query Embeddings

```bash
python embeddings-management/scripts/read_embeddings.py
```

Interactive menu for:
- Reading all embeddings
- Reading by specific IDs
- Semantic search by text query
- Search with metadata filters
- Viewing raw embedding vectors

### 3. Delete Embeddings

```bash
python embeddings-management/scripts/delete_embeddings.py
```

Interactive menu for:
- Deleting by IDs
- Deleting by metadata filters
- Clearing entire collections
- Bulk delete operations

### 4. Get Collection Info

```bash
python embeddings-management/scripts/get_info.py
```

Shows:
- Collection statistics
- Document counts
- Metadata summaries
- Storage information

### 5. Run Examples

```bash
# Simple embedding example
python embeddings-management/examples/get_embeddings.py

# Complete CRUD test
python embeddings-management/examples/test_complete_crud.py
```

### 6. Run Tests

```bash
# Individual tests
python embeddings-management/tests/test_create.py
python embeddings-management/tests/test_read.py
python embeddings-management/tests/test_update.py
python embeddings-management/tests/test_delete.py

# Complete test suite
python embeddings-management/tests/test_complete_crud.py
```

## Prerequisites

1. **Ollama** running with embedding model:
   ```bash
   ollama pull all-minilm
   ```

2. **Dependencies** installed:
   ```bash
   pip install -r requirements.txt
   ```

3. **Project structure**: Run from project root directory

## Configuration

Scripts use the parent project's configuration:
- `config.py`: Ollama and ChromaDB settings
- `db/chromadb_service.py`: ChromaDB service
- `utils.py`: Utility functions

## Data Sources

### Current Support
- **JSON files**: `mock-data/payment_support_data.json`
- **Format**: Array of objects with `id`, `question`, `answer`, `category`, `keywords`

### Adding New Data Sources
1. Create new script in `scripts/`
2. Use `utils.json_to_embeddings()` or `utils.text_to_embeddings()`
3. Store using `ChromaDBService.create()`

## Integration with RAG Service

This module manages the knowledge base that the RAG service consumes:

```
embeddings-management/     →    ChromaDB    →    langgraph/
(Data Management)              (Storage)         (RAG Service)
```

- **embeddings-management**: Creates and maintains embeddings
- **ChromaDB**: Stores embeddings
- **langgraph**: Queries embeddings for RAG

## Troubleshooting

### Import Errors
- Ensure running from project root
- Check that parent directories are accessible
- Verify all dependencies are installed

### Ollama Connection Errors
- Ensure Ollama is running: `ollama serve`
- Check model availability: `ollama list`
- Verify API URL in `config.py`

### ChromaDB Errors
- Check `chroma_db/` directory exists and is writable
- Verify collection names are valid
- Check disk space for large collections

### Path Issues
- All scripts use relative paths from project root
- Use `Path(__file__).parent.parent.parent` to get project root
- Ensure `sys.path.insert(0, str(parent_dir))` is working

## Best Practices

1. **Data Backup**: Backup `chroma_db/` directory before bulk operations
2. **Testing**: Test scripts on small datasets first
3. **Monitoring**: Use `get_info.py` to monitor collection health
4. **Validation**: Verify embeddings after creation with `read_embeddings.py`
5. **Cleanup**: Use `delete_embeddings.py` to remove test data

## Future Enhancements

- Support for more data formats (CSV, XML, databases)
- Batch processing for large datasets
- Incremental updates (only process new/changed data)
- Data validation and quality checks
- Automated backup and restore
- Performance monitoring and optimization
