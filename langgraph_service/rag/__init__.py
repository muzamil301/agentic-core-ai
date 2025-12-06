"""
RAG (Retrieval Augmented Generation) module for LangGraph service.

This module provides components for retrieving relevant documents from ChromaDB.
"""

from langgraph_service.rag.retriever import ChromaDBRetriever

__all__ = [
    "ChromaDBRetriever",
]

