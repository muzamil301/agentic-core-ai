"""
Context formatting utilities for RAG.

This module provides functions to format retrieved documents into
a context string for LLM consumption.
"""

from typing import List, Dict, Any
from langgraph.config.settings import MAX_CONTEXT_LENGTH


def format_context(
    retrieved_docs: List[Dict[str, Any]],
    max_length: int = MAX_CONTEXT_LENGTH,
    include_metadata: bool = True,
    include_scores: bool = False
) -> str:
    """
    Format retrieved documents into a context string.
    
    Args:
        retrieved_docs: List of retrieved documents with keys:
            - text: Document text
            - metadata: Document metadata (optional)
            - score: Similarity score (optional)
            - id: Document ID (optional)
        max_length: Maximum character length for context
        include_metadata: Whether to include metadata in context
        include_scores: Whether to include similarity scores (for debugging)
    
    Returns:
        Formatted context string
    """
    if not retrieved_docs:
        return "No relevant context found."
    
    context_parts = []
    current_length = 0
    
    for i, doc in enumerate(retrieved_docs, 1):
        text = doc.get("text", "")
        metadata = doc.get("metadata", {})
        score = doc.get("score", None)
        
        # Build document entry
        entry_parts = [f"[{i}]"]
        
        # Add metadata if requested
        if include_metadata and metadata:
            category = metadata.get("category", "")
            if category:
                entry_parts.append(f"Category: {category}")
        
        # Add score if requested (for debugging)
        if include_scores and score is not None:
            entry_parts.append(f"(Similarity: {score:.2f})")
        
        entry_parts.append(text)
        entry = " ".join(entry_parts)
        
        # Check if adding this entry would exceed max length
        if current_length + len(entry) > max_length and context_parts:
            break
        
        context_parts.append(entry)
        current_length += len(entry)
    
    if not context_parts:
        return "No relevant context found."
    
    return "\n\n".join(context_parts)




