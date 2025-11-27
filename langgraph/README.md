# LangGraph RAG Service

A complete RAG (Retrieval Augmented Generation) service layer built with LangGraph for building stateful, multi-step LLM applications.

## Overview

This service provides a modular, monorepo-ready RAG implementation that:
- Retrieves relevant documents from ChromaDB using semantic search
- Augments user queries with retrieved context
- Generates responses using Ollama LLM
- Maintains conversation history
- Provides a clean service interface

## Architecture

```
langgraph/
├── config/              # Configuration and settings
│   ├── __init__.py
│   └── settings.py      # All configuration constants
├── rag/                 # RAG components
│   ├── __init__.py
│   ├── retriever.py     # ChromaDB retriever
│   ├── prompts.py       # Prompt templates
│   └── context_formatter.py  # Context formatting
├── llm/                 # LLM integration
│   ├── __init__.py
│   └── ollama_chat.py   # Ollama chat client
├── graph/               # LangGraph definition
│   ├── __init__.py
│   ├── state.py         # State schema
│   ├── nodes.py         # Graph nodes
│   └── graph.py         # Graph compilation
├── service/             # Service layer
│   ├── __init__.py
│   └── rag_service.py   # High-level RAG service
├── chat.py              # CLI chat interface
└── README.md            # This file
```

## Installation

1. Install dependencies:
```bash
pip install langgraph langchain langchain-community langchain-core
```

2. Ensure prerequisites:
   - Ollama running with a chat model (e.g., `llama3.2`)
   - ChromaDB with embeddings stored (run `payment_support_embeddings.py`)

## Usage

### As a Service (Programmatic)

```python
from langgraph.service.rag_service import RAGService

# Initialize service
service = RAGService()

# Chat
result = service.chat("What is my daily transaction limit?")
print(result["response"])

# With conversation history
result = service.chat("How do I check it?")  # Understands "it" from context
print(result["response"])

# Reset conversation
service.reset_conversation()
```

### CLI Interface

```bash
python -m langgraph.chat
```

This starts an interactive chat session.

## Configuration

All configuration is in `config/settings.py`. You can override via environment variables:

- `OLLAMA_CHAT_API_URL`: Ollama chat API URL
- `CHAT_MODEL`: Chat model name (default: `llama3.2`)
- `RETRIEVAL_TOP_K`: Number of documents to retrieve (default: 3)
- `MAX_CONTEXT_LENGTH`: Max context length (default: 2000)
- `ENABLE_CONVERSATION_HISTORY`: Enable/disable history (default: true)
- `MAX_HISTORY_LENGTH`: Max conversation turns (default: 5)
- `RAG_COLLECTION_NAME`: ChromaDB collection name (default: `payment_support`)

## Components

### Retriever (`rag/retriever.py`)
- Wraps ChromaDBService for semantic search
- Returns top-k relevant documents with scores

### LLM Client (`llm/ollama_chat.py`)
- Interfaces with Ollama chat API
- Handles message formatting and API calls

### Graph Nodes (`graph/nodes.py`)
- `retrieve_node`: Retrieves documents from ChromaDB
- `format_context_node`: Formats retrieved docs into context
- `generate_node`: Generates response using LLM
- `respond_node`: Finalizes response and updates history

### Service Layer (`service/rag_service.py`)
- High-level API for RAG operations
- Manages conversation history
- Provides simple chat interface

## Example Flow

1. User asks: "What is my daily transaction limit?"
2. **Retrieve Node**: Searches ChromaDB, finds 3 relevant docs
3. **Format Context Node**: Formats docs into context string
4. **Generate Node**: Sends context + query to Ollama, gets response
5. **Respond Node**: Updates conversation history, returns response

## Integration with Parent Project

This service is designed to work alongside the existing embeddings project:
- Uses existing `ChromaDBService` from `db/chromadb_service.py`
- Uses existing `text_to_embeddings` from `utils.py`
- References parent `config.py` for embedding settings
- Maintains independence as a service layer

## Testing

```python
from langgraph.service.rag_service import RAGService

service = RAGService()

# Test query
result = service.chat("What is my daily transaction limit?")
assert "limit" in result["response"].lower()
assert len(result["retrieved_docs"]) > 0
```

## Future Enhancements

- Response streaming
- Confidence scoring
- Source citation
- Metadata filtering
- Hybrid search (keyword + semantic)
- Web interface (Streamlit/Gradio)




