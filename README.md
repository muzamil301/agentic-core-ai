# Embeddings & RAG Monorepo

A complete monorepo for embeddings management and RAG (Retrieval Augmented Generation) applications using ChromaDB and LangGraph.

## Overview

This monorepo provides:
- **Embeddings Management**: Complete CRUD operations for embeddings in ChromaDB
- **RAG Service**: LangGraph-powered RAG service for chat applications
- **Shared Infrastructure**: Common database services and utilities

## Monorepo Structure

```
embeddings-py/
├── embeddings-management/       # 📁 Embeddings CRUD operations
│   ├── scripts/                 # Production scripts
│   ├── examples/                # Learning examples
│   ├── tests/                   # Unit tests
│   └── README.md                # Embeddings management docs
│
├── langgraph/                   # 🤖 RAG service with LangGraph
│   ├── config/                  # RAG configuration
│   ├── rag/                     # RAG components
│   ├── llm/                     # LLM integration
│   ├── graph/                   # LangGraph definition
│   ├── service/                 # Service layer
│   ├── chat.py                  # CLI interface
│   └── README.md                # RAG service docs
│
├── db/                          # 🗄️ Shared database layer
│   └── chromadb_service.py      # ChromaDB service
├── mock-data/                   # 📄 Sample data
│   └── payment_support_data.json
├── config.py                    # 🔧 Shared configuration
├── utils.py                     # 🛠️ Shared utilities
└── requirements.txt             # 📦 Dependencies
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

### 1. Setup Embeddings (Knowledge Base)

```bash
# Create embeddings from sample data
python embeddings-management/scripts/payment_support_embeddings.py

# Verify embeddings were created
python embeddings-management/scripts/read_embeddings.py
```

### 2. Use RAG Chat Service

```bash
# Interactive chat with RAG
python langgraph/chat.py

# Or run programmatic example
python langgraph/example.py
```

## Components

### 🗄️ Embeddings Management (`embeddings-management/`)
Manages the knowledge base:
- **Create**: Generate embeddings from data sources
- **Read**: Query and inspect embeddings  
- **Update**: Modify existing embeddings
- **Delete**: Remove outdated embeddings

```bash
# Create embeddings
python embeddings-management/scripts/payment_support_embeddings.py

# Query embeddings
python embeddings-management/scripts/read_embeddings.py

# Delete embeddings
python embeddings-management/scripts/delete_embeddings.py
```

### 🤖 RAG Service (`langgraph/`)
LangGraph-powered chat service with intelligent routing:
- **Smart Routing**: Automatically decides RAG vs direct answers
- **Web UI**: Modern Streamlit-based chat interface
- **Query Classification**: Handles payments, greetings, general questions
- **Conversation**: Multi-turn chat with history

```bash
# 🌐 Web UI (Recommended)
python langgraph/run_ui.py

# 💻 CLI chat interface
python langgraph/chat.py

# 🧠 Test intelligent routing
python langgraph/example_routing.py

# 📝 Programmatic usage
from langgraph.service.rag_service import RAGService
service = RAGService()
result = service.chat("What is my daily transaction limit?")
```

### 🛠️ Shared Infrastructure
- **Database**: `db/chromadb_service.py` - ChromaDB operations
- **Utilities**: `utils.py` - Embedding generation
- **Config**: `config.py` - Shared settings

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

