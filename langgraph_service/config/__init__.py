"""
Configuration module for LangGraph RAG service.

This module provides centralized configuration settings.
"""

from langgraph_service.config.settings import (
    # Ollama Settings
    OLLAMA_EMBED_API_URL,
    OLLAMA_CHAT_API_URL,
    EMBEDDING_MODEL,
    CHAT_MODEL,
    OLLAMA_TIMEOUT,
    
    # ChromaDB Settings
    CHROMADB_PERSIST_DIRECTORY,
    COLLECTION_NAME,
    
    # RAG Settings
    RETRIEVAL_TOP_K,
    SIMILARITY_THRESHOLD,
    MAX_CONTEXT_LENGTH,
    
    # Conversation Settings
    ENABLE_CONVERSATION_HISTORY,
    MAX_HISTORY_LENGTH,
)

__all__ = [
    "OLLAMA_EMBED_API_URL",
    "OLLAMA_CHAT_API_URL",
    "EMBEDDING_MODEL",
    "CHAT_MODEL",
    "OLLAMA_TIMEOUT",
    "CHROMADB_PERSIST_DIRECTORY",
    "COLLECTION_NAME",
    "RETRIEVAL_TOP_K",
    "SIMILARITY_THRESHOLD",
    "MAX_CONTEXT_LENGTH",
    "ENABLE_CONVERSATION_HISTORY",
    "MAX_HISTORY_LENGTH",
]

