"""
RAG (Retrieval Augmented Generation) components.

This module contains:
- Retriever: Interface for retrieving relevant documents from ChromaDB
- Prompts: Prompt templates for LLM interactions
- Context Formatter: Utilities for formatting retrieved context
"""

from .retriever import ChromaDBRetriever
from .prompts import SYSTEM_PROMPT, CONTEXT_FORMAT, USER_QUERY_FORMAT
from .context_formatter import format_context

__all__ = [
    "ChromaDBRetriever",
    "SYSTEM_PROMPT",
    "CONTEXT_FORMAT",
    "USER_QUERY_FORMAT",
    "format_context",
]




