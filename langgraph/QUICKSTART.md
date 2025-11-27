# Quick Start Guide

## Prerequisites

1. **Ollama with Chat Model**
   ```bash
   # Install Ollama (if not already installed)
   # Visit: https://ollama.ai
   
   # Pull a chat model
   ollama pull llama3.2
   # or
   ollama pull mistral
   ```

2. **ChromaDB with Embeddings**
   ```bash
   # From project root, ensure embeddings are stored
   python payment_support_embeddings.py
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Option 1: CLI Chat Interface

```bash
# From project root
python -m langgraph.chat
```

Or:

```bash
cd langgraph
python chat.py
```

### Option 2: Programmatic Usage

```python
from langgraph.service.rag_service import RAGService

# Initialize
service = RAGService()

# Chat
result = service.chat("What is my daily transaction limit?")
print(result["response"])
```

### Option 3: Run Example

```bash
python -m langgraph.example
```

## Configuration

Edit `langgraph/config/settings.py` or set environment variables:

```bash
export CHAT_MODEL="llama3.2"
export RETRIEVAL_TOP_K=5
export ENABLE_CONVERSATION_HISTORY=true
```

## Troubleshooting

### "Failed to initialize RAG service"
- Ensure Ollama is running: `ollama serve`
- Check if chat model is available: `ollama list`
- Verify ChromaDB has data: Check `chroma_db/` directory

### "No results found"
- Ensure embeddings are stored: Run `payment_support_embeddings.py`
- Check collection name matches in `config/settings.py`

### Import Errors
- Ensure you're running from project root
- Check that all dependencies are installed: `pip install -r requirements.txt`



