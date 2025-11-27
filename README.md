# 🤖 RAG Chat System with LangGraph

A complete **Retrieval Augmented Generation (RAG)** chat system built with **LangGraph**, **Ollama**, and **ChromaDB**. This project demonstrates intelligent query routing, embeddings-based retrieval, and conversational AI for payment support scenarios.

## 🎯 **What This Project Does**

- **Intelligent Query Classification**: Automatically determines if queries need RAG, direct answers, or simple greetings
- **Embeddings-Based Retrieval**: Uses ChromaDB to find relevant context from payment support knowledge base
- **LangGraph Workflow**: Implements stateful conversation flows with conditional routing
- **Multiple UI Options**: Streamlit web app, standalone HTML demo, and CLI interface
- **Monorepo Structure**: Organized codebase with separate services for embeddings, RAG, frontend, and API

## 🏗️ **Architecture Overview**

```
embeddings-py/
├── 📁 embeddings-management/     # CRUD operations for embeddings
├── 📁 langgraph/                 # RAG service with LangGraph
├── 📁 frontend/                  # React chat interface (optional)
├── 📁 api/                       # FastAPI backend (optional)
├── 📄 standalone_chat.html       # Self-contained demo
└── 📄 simple_frontend.html       # HTML chat interface
```

### **Core Components**

1. **LangGraph RAG Pipeline**:
   - Query Classification → Retrieval → Context Formatting → Response Generation
   - Conditional routing based on query type (RAG/Direct/Greeting)

2. **ChromaDB Vector Store**:
   - Stores payment support embeddings
   - Semantic search for relevant context

3. **Ollama Integration**:
   - Local LLM for chat responses (`llama3.2`)
   - Embeddings generation (`all-minilm`)

## 🚀 **Quick Start**

### **Prerequisites**

1. **Install Ollama**:
   ```bash
   # Download from https://ollama.ai
   ollama serve
   ollama pull llama3.2
   ollama pull all-minilm
   ```

2. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Embeddings** (if not already done):
   ```bash
   python embeddings-management/scripts/payment_support_embeddings.py
   ```

### **Option 1: Streamlit UI (Recommended)**

The easiest way to use the full RAG system:

```bash
python langgraph/run_ui.py
```

Then open: **http://localhost:8501**

### **Option 2: Standalone HTML Demo**

For a quick demo without any server setup:

```bash
open standalone_chat.html
```

### **Option 3: CLI Interface**

For command-line interaction:

```bash
python langgraph/chat.py
```

## 🎨 **User Interface Options**

### **1. Streamlit Web App** ⭐ *Recommended*
- **Full RAG functionality**
- **Real-time chat interface**
- **Conversation history**
- **Query type indicators**
- **No setup required**

### **2. Standalone HTML Demo**
- **Beautiful chat interface**
- **Simulated RAG responses**
- **Works offline**
- **No dependencies**

### **3. React Frontend** (Optional)
- **Modern React interface**
- **Real-time WebSocket chat**
- **Requires npm setup**

## 🔧 **Configuration**

### **Main Settings** (`config.py`)
```python
# Ollama Configuration
OLLAMA_BASE_URL = "http://localhost:11434"
EMBEDDING_MODEL = "all-minilm"
CHAT_MODEL = "llama3.2"

# ChromaDB Configuration
CHROMADB_PERSIST_DIRECTORY = "./chroma_db"
COLLECTION_NAME = "payment_support"

# RAG Settings
RETRIEVAL_TOP_K = 3
SIMILARITY_THRESHOLD = 0.7
```

### **LangGraph Settings** (`langgraph/config/settings.py`)
```python
# Additional LangGraph-specific settings
MAX_CONTEXT_LENGTH = 4000
ENABLE_CONVERSATION_HISTORY = True
MAX_HISTORY_LENGTH = 10
```

## 💬 **How to Use**

### **Example Queries**

**RAG-Enhanced Queries** (searches knowledge base):
- "What is my daily transaction limit?"
- "How do I block my card?"
- "How long do international transfers take?"
- "Tell me about account tiers"

**Direct Answers** (no retrieval needed):
- "What's 2+2?"
- "What's the weather like?"
- "Tell me a joke"

**Greetings**:
- "Hello, how are you?"
- "Hi there!"
- "Good morning"

### **Chat Features**

- **Intelligent Routing**: System automatically decides whether to use RAG or provide direct answers
- **Conversation Memory**: Maintains context across the conversation
- **Source Attribution**: Shows which documents were used for RAG responses
- **Query Classification**: Displays how each query was classified (RAG/Direct/Greeting)

## 🛠️ **Development**

### **Project Structure**

```
embeddings-py/
├── embeddings-management/        # Embeddings CRUD operations
│   ├── scripts/                 # Embedding creation/management scripts
│   ├── examples/                # Usage examples
│   └── tests/                   # Test files
├── langgraph/                   # RAG service layer
│   ├── config/                  # Configuration files
│   ├── rag/                     # RAG components
│   ├── llm/                     # LLM clients
│   ├── graph/                   # LangGraph definitions
│   ├── service/                 # High-level services
│   └── ui/                      # Streamlit interface
├── frontend/                    # React frontend (optional)
├── api/                         # FastAPI backend (optional)
├── db/                          # Database services
└── utils/                       # Utility functions
```

### **Key Files**

- **`langgraph/service/rag_service.py`**: Main RAG service
- **`langgraph/graph/graph.py`**: LangGraph workflow definition
- **`langgraph/graph/nodes.py`**: Individual workflow nodes
- **`langgraph/ui/streamlit_app.py`**: Streamlit interface
- **`db/chromadb_service.py`**: ChromaDB integration

### **Adding New Knowledge**

1. **Add documents to embeddings**:
   ```bash
   # Edit the knowledge base in:
   embeddings-management/scripts/payment_support_embeddings.py
   
   # Then regenerate embeddings:
   python embeddings-management/scripts/payment_support_embeddings.py
   ```

2. **Verify embeddings**:
   ```bash
   python embeddings-management/scripts/read_embeddings.py
   ```

## 🔍 **Troubleshooting**

### **Common Issues**

1. **"RAG service not initialized"**:
   ```bash
   # Check Ollama is running:
   ollama list
   
   # Restart Ollama:
   ollama serve
   ```

2. **"No embeddings found"**:
   ```bash
   # Create embeddings:
   python embeddings-management/scripts/payment_support_embeddings.py
   ```

3. **Architecture errors (Apple Silicon)**:
   ```bash
   # Use Streamlit UI instead of FastAPI:
   python langgraph/run_ui.py
   ```

4. **Port conflicts**:
   ```bash
   # Check what's using port 8501:
   lsof -i :8501
   
   # Kill process if needed:
   kill -9 <PID>
   ```

### **Debug Tools**

- **Connection diagnostics**: `python debug_connection.py`
- **Test RAG service**: `python test_simple_chat.py`
- **Check embeddings**: `python embeddings-management/scripts/read_embeddings.py`

## 📚 **Learning Resources**

### **Understanding RAG**
- **Retrieval**: Finding relevant documents using semantic similarity
- **Augmentation**: Adding retrieved context to the prompt
- **Generation**: LLM generates response using context + query

### **LangGraph Concepts**
- **Nodes**: Individual processing steps (classify, retrieve, generate)
- **Edges**: Connections between nodes
- **State**: Shared data structure passed between nodes
- **Conditional Routing**: Dynamic path selection based on query type

### **Key Technologies**
- **ChromaDB**: Vector database for embeddings storage
- **Ollama**: Local LLM serving platform
- **LangGraph**: Framework for building stateful AI workflows
- **Streamlit**: Python web app framework

## 🤝 **Contributing**

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-feature`
3. **Make changes and test**: `python langgraph/run_ui.py`
4. **Commit changes**: `git commit -m "Add new feature"`
5. **Push and create PR**: `git push origin feature/new-feature`

## 📄 **License**

This project is for educational purposes. Feel free to use and modify for learning about RAG systems and LangGraph.

## 🆘 **Support**

- **Check the troubleshooting section above**
- **Run diagnostics**: `python debug_connection.py`
- **Use Streamlit UI** for the most reliable experience
- **Check Ollama status**: `ollama list`

---

**Happy RAG Building!** 🚀

*This project demonstrates a complete RAG pipeline with intelligent query routing, perfect for learning how modern AI systems combine retrieval and generation for enhanced responses.*