# LangGraph Service Structure

## Directory Organization

```
langgraph/
├── __init__.py                 # Package initialization
├── README.md                    # Main documentation
├── QUICKSTART.md               # Quick start guide
├── STRUCTURE.md                # This file
│
├── config/                     # Configuration layer
│   ├── __init__.py
│   └── settings.py            # All configuration constants
│
├── rag/                        # RAG components
│   ├── __init__.py
│   ├── retriever.py           # ChromaDB retriever wrapper
│   ├── prompts.py             # Prompt templates
│   └── context_formatter.py   # Context formatting utilities
│
├── llm/                        # LLM integration
│   ├── __init__.py
│   └── ollama_chat.py         # Ollama chat client
│
├── graph/                      # LangGraph definition
│   ├── __init__.py
│   ├── state.py               # State schema
│   ├── nodes.py               # Graph nodes (functions)
│   └── graph.py               # Graph compilation
│
├── service/                    # Service layer
│   ├── __init__.py
│   └── rag_service.py         # High-level RAG service API
│
├── chat.py                     # CLI chat interface
└── example.py                  # Usage examples
```

## Design Principles

### 1. **Separation of Concerns**
- **config/**: All configuration in one place
- **rag/**: RAG-specific logic (retrieval, prompts, formatting)
- **llm/**: LLM interaction logic
- **graph/**: LangGraph-specific code
- **service/**: High-level API

### 2. **Monorepo-Ready**
- Self-contained service layer
- Minimal dependencies on parent project
- Can be easily extracted or reused
- Clear boundaries between layers

### 3. **Configuration Management**
- All settings in `config/settings.py`
- Environment variable support
- Fallback to parent project config where needed
- Easy to override for different environments

### 4. **Service Interface**
- High-level `RAGService` class
- Simple API: `service.chat(query)`
- Hides complexity of graph management
- Easy to integrate into other services

## Component Responsibilities

### Config Layer (`config/`)
- **Purpose**: Centralized configuration
- **Files**: `settings.py`
- **Exports**: All configuration constants
- **Dependencies**: None (base layer)

### RAG Layer (`rag/`)
- **Purpose**: Retrieval and context preparation
- **Components**:
  - `retriever.py`: ChromaDB queries
  - `prompts.py`: Prompt templates
  - `context_formatter.py`: Document formatting
- **Dependencies**: `config/`, parent `db/`, parent `utils/`

### LLM Layer (`llm/`)
- **Purpose**: LLM interaction
- **Components**:
  - `ollama_chat.py`: Ollama API client
- **Dependencies**: `config/`

### Graph Layer (`graph/`)
- **Purpose**: LangGraph definition and execution
- **Components**:
  - `state.py`: State schema
  - `nodes.py`: Node implementations
  - `graph.py`: Graph compilation
- **Dependencies**: `rag/`, `llm/`, `config/`

### Service Layer (`service/`)
- **Purpose**: High-level API
- **Components**:
  - `rag_service.py`: Main service interface
- **Dependencies**: `graph/`

### Interface Layer (root)
- **Purpose**: User-facing interfaces
- **Components**:
  - `chat.py`: CLI interface
  - `example.py`: Usage examples
- **Dependencies**: `service/`

## Data Flow

```
User Query
    ↓
chat.py / example.py
    ↓
service/rag_service.py
    ↓
graph/graph.py (compiled graph)
    ↓
graph/nodes.py
    ├─→ rag/retriever.py → ChromaDB
    ├─→ rag/context_formatter.py
    └─→ llm/ollama_chat.py → Ollama
    ↓
Response
```

## Integration Points

### With Parent Project
- Uses `db/chromadb_service.py` for ChromaDB access
- Uses `utils.py` for embedding generation
- References parent `config.py` for embedding settings
- Maintains independence as a service

### External Dependencies
- **LangGraph**: Graph framework
- **LangChain**: Core abstractions
- **Ollama**: LLM provider
- **ChromaDB**: Vector database

## Extension Points

### Adding New Features
1. **New Retrieval Strategy**: Add to `rag/retriever.py`
2. **New Prompt Templates**: Add to `rag/prompts.py`
3. **New Graph Nodes**: Add to `graph/nodes.py`
4. **New LLM Provider**: Add to `llm/` directory
5. **New Interface**: Add to root (e.g., `api.py`, `web.py`)

### Configuration
- All settings in `config/settings.py`
- Environment variables supported
- Easy to add new configuration options

## Testing Strategy

### Unit Tests
- Test each component in isolation
- Mock external dependencies (Ollama, ChromaDB)
- Test configuration loading

### Integration Tests
- Test full RAG pipeline
- Test service interface
- Test graph execution

### Example Usage
- `example.py` demonstrates basic usage
- Can be used for manual testing

## Future Enhancements

1. **Streaming**: Add streaming support to `llm/ollama_chat.py`
2. **Caching**: Add caching layer in `service/`
3. **Monitoring**: Add observability in `graph/nodes.py`
4. **Validation**: Add validation node in `graph/nodes.py`
5. **Fallback**: Add fallback mechanisms
6. **Web API**: Add REST API interface
7. **Web UI**: Add Streamlit/Gradio interface



