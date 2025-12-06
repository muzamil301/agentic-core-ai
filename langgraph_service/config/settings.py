"""
Configuration settings for LangGraph RAG service.

All configuration constants are defined here for easy management.
"""

import os
from pathlib import Path

# ============================================================================
# Ollama API Configuration
# ============================================================================

# Embeddings API (for generating embeddings)
OLLAMA_EMBED_API_URL = os.getenv(
    "OLLAMA_EMBED_API_URL",
    "http://localhost:11434/api/embed"
)

# Chat API (for generating responses)
OLLAMA_CHAT_API_URL = os.getenv(
    "OLLAMA_CHAT_API_URL",
    "http://localhost:11434/api/chat"
)

# Model names
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-minilm")
CHAT_MODEL = os.getenv("CHAT_MODEL", "llama3")  # Changed from "llama3.2" to "llama3"

# Timeout settings (in seconds)
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "30"))

# ============================================================================
# ChromaDB Configuration
# ============================================================================

# Persistence directory for ChromaDB
# Default: ./chroma_db (relative to project root)
CHROMADB_PERSIST_DIRECTORY = os.getenv(
    "CHROMADB_PERSIST_DIRECTORY",
    str(Path(__file__).parent.parent.parent / "chroma_db")
)

# Collection name for storing embeddings
COLLECTION_NAME = os.getenv(
    "COLLECTION_NAME",
    "customer_support_embeddings"
)

# ============================================================================
# RAG Configuration
# ============================================================================

# Number of documents to retrieve from ChromaDB
RETRIEVAL_TOP_K = int(os.getenv("RETRIEVAL_TOP_K", "3"))

# Minimum similarity score threshold (0.0 to 1.0)
# Documents below this threshold will be filtered out
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.5"))

# Maximum context length (in characters)
# Used to limit the size of context passed to LLM
MAX_CONTEXT_LENGTH = int(os.getenv("MAX_CONTEXT_LENGTH", "2000"))

# ============================================================================
# Conversation Settings
# ============================================================================

# Enable conversation history
ENABLE_CONVERSATION_HISTORY = os.getenv(
    "ENABLE_CONVERSATION_HISTORY",
    "true"
).lower() == "true"

# Maximum number of messages to keep in history
MAX_HISTORY_LENGTH = int(os.getenv("MAX_HISTORY_LENGTH", "10"))

# ============================================================================
# Validation
# ============================================================================

def validate_settings():
    """
    Validate configuration settings.
    
    Raises:
        ValueError: If any setting has an invalid value.
    """
    errors = []
    
    # Validate timeout
    if OLLAMA_TIMEOUT <= 0:
        errors.append("OLLAMA_TIMEOUT must be greater than 0")
    
    # Validate top_k
    if RETRIEVAL_TOP_K <= 0:
        errors.append("RETRIEVAL_TOP_K must be greater than 0")
    
    # Validate similarity threshold
    if not 0.0 <= SIMILARITY_THRESHOLD <= 1.0:
        errors.append("SIMILARITY_THRESHOLD must be between 0.0 and 1.0")
    
    # Validate max context length
    if MAX_CONTEXT_LENGTH <= 0:
        errors.append("MAX_CONTEXT_LENGTH must be greater than 0")
    
    # Validate max history length
    if MAX_HISTORY_LENGTH <= 0:
        errors.append("MAX_HISTORY_LENGTH must be greater than 0")
    
    if errors:
        raise ValueError("Configuration validation failed:\n" + "\n".join(f"  - {e}" for e in errors))
    
    return True


def get_settings_summary():
    """
    Get a summary of all configuration settings.
    
    Returns:
        dict: Dictionary containing all settings.
    """
    return {
        "ollama": {
            "embed_api_url": OLLAMA_EMBED_API_URL,
            "chat_api_url": OLLAMA_CHAT_API_URL,
            "embedding_model": EMBEDDING_MODEL,
            "chat_model": CHAT_MODEL,
            "timeout": OLLAMA_TIMEOUT,
        },
        "chromadb": {
            "persist_directory": CHROMADB_PERSIST_DIRECTORY,
            "collection_name": COLLECTION_NAME,
        },
        "rag": {
            "retrieval_top_k": RETRIEVAL_TOP_K,
            "similarity_threshold": SIMILARITY_THRESHOLD,
            "max_context_length": MAX_CONTEXT_LENGTH,
        },
        "conversation": {
            "enable_history": ENABLE_CONVERSATION_HISTORY,
            "max_history_length": MAX_HISTORY_LENGTH,
        },
    }

