# LangGraph RAG Service

A service layer for building RAG (Retrieval Augmented Generation) systems using LangGraph, ChromaDB, and Ollama.

## 📁 Directory Structure

```
langgraph/
├── __init__.py              # Package initialization
├── config/                  # Configuration module
│   ├── __init__.py
│   └── settings.py          # All configuration settings
└── README.md                # This file
```

## 🎯 Purpose

This service provides:
- **Query Classification**: Intelligently classify user queries
- **Document Retrieval**: Retrieve relevant context from ChromaDB
- **Response Generation**: Generate responses using Ollama LLM
- **Graph-Based Routing**: Route queries through different paths using LangGraph

## ⚙️ Configuration

All configuration is managed in `config/settings.py`. Settings can be:
- Set directly in the file
- Overridden via environment variables
- Validated using `validate_settings()`

### Key Settings

- **Ollama API URLs**: Embeddings and chat endpoints
- **Model Names**: Embedding and chat models
- **ChromaDB**: Persistence directory and collection name
- **RAG Parameters**: Top-K retrieval, similarity threshold, context length
- **Conversation**: History management settings

## 🚀 Getting Started

This is Milestone 1 - Basic Components Setup. The service is being built step by step.

### Current Status

✅ **Milestone 1 Complete**: Basic directory structure and configuration

### Next Steps

- Milestone 2: Query Classification
- Milestone 3: Document Retrieval
- Milestone 4: LLM Integration
- ... (see `LANGGRAPH_BUILD_PLAN.md` for full plan)

## 📝 Usage Example

```python
from langgraph.config import (
    OLLAMA_CHAT_API_URL,
    CHAT_MODEL,
    CHROMADB_PERSIST_DIRECTORY,
    COLLECTION_NAME,
)

# Access configuration
print(f"Chat API: {OLLAMA_CHAT_API_URL}")
print(f"Model: {CHAT_MODEL}")
print(f"ChromaDB: {CHROMADB_PERSIST_DIRECTORY}")
```

## 🧪 Testing

Run the milestone test:
```bash
python testing/test_milestone_1.py
```

## 📚 Documentation

See `LANGGRAPH_BUILD_PLAN.md` for the complete build plan and milestones.

