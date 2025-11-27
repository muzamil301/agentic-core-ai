"""
Configuration settings for LangGraph RAG service.

This module contains all configuration constants used by the RAG service.
Separated from the main embeddings config to maintain service independence.
"""

import os
from pathlib import Path

# Ollama Chat Configuration
OLLAMA_CHAT_API_URL = os.getenv("OLLAMA_CHAT_API_URL", "http://localhost:11434/api/chat")
CHAT_MODEL = os.getenv("CHAT_MODEL", "llama3.2")  # or "mistral", "qwen2", etc.
CHAT_TIMEOUT = int(os.getenv("CHAT_TIMEOUT", "30"))  # seconds

# RAG Configuration
RETRIEVAL_TOP_K = int(os.getenv("RETRIEVAL_TOP_K", "3"))  # Number of documents to retrieve
MAX_CONTEXT_LENGTH = int(os.getenv("MAX_CONTEXT_LENGTH", "2000"))  # Max characters in context
ENABLE_CONVERSATION_HISTORY = os.getenv("ENABLE_CONVERSATION_HISTORY", "true").lower() == "true"
MAX_HISTORY_LENGTH = int(os.getenv("MAX_HISTORY_LENGTH", "5"))  # Number of previous exchanges to keep
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.0"))  # Minimum similarity score (0.0 = no filter)

# ChromaDB Configuration (references parent project config)
# These can be overridden via environment variables
COLLECTION_NAME = os.getenv("RAG_COLLECTION_NAME", "payment_support")
CHROMADB_PERSIST_DIRECTORY = os.getenv(
    "CHROMADB_PERSIST_DIRECTORY",
    str(Path(__file__).parent.parent.parent / "chroma_db")
)

# Embedding Configuration (references parent project)
# Import from parent config to reuse existing settings
try:
    import sys
    from pathlib import Path
    parent_dir = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(parent_dir))
    from config import OLLAMA_API_URL as EMBEDDING_API_URL, EMBEDDING_MODEL, OLLAMA_TIMEOUT as EMBEDDING_TIMEOUT
except ImportError:
    # Fallback if parent config not available
    EMBEDDING_API_URL = os.getenv("OLLAMA_EMBED_API_URL", "http://localhost:11434/api/embed")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-minilm")
    EMBEDDING_TIMEOUT = int(os.getenv("EMBEDDING_TIMEOUT", "15"))




