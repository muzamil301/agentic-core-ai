"""
LangGraph State Schema Definition.

This module defines the state structure used throughout the graph.
"""

from typing import TypedDict, List, Dict, Any, Annotated

# Try different import paths for add_messages
try:
    from langgraph.graph.message import add_messages
except ImportError:
    try:
        from langgraph.prebuilt import add_messages
    except ImportError:
        try:
            from langchain_core.messages import add_messages
        except ImportError:
            # Fallback: create a simple add_messages function
            def add_messages(left: List[Dict], right: List[Dict]) -> List[Dict]:
                """Simple message addition fallback."""
                return left + right


class GraphState(TypedDict):
    """
    State schema for the RAG LangGraph.
    
    This state is passed between nodes and contains all information
    needed for the RAG pipeline.
    """
    # Conversation history (managed by LangGraph's add_messages)
    messages: Annotated[List[Dict[str, str]], add_messages]
    
    # Current user query
    query: str
    
    # Retrieved documents from ChromaDB
    retrieved_docs: List[Dict[str, Any]]
    
    # Formatted context string
    context: str
    
    # Generated response from LLM
    response: str
    
    # Additional metadata (errors, timings, etc.)
    metadata: Dict[str, Any]




