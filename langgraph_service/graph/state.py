"""
LangGraph State Definition

This module defines the GraphState TypedDict that will flow through
the LangGraph. All nodes will receive and update this state.
"""

from typing import TypedDict, List, Dict, Any, Annotated

# Try to import add_messages from different possible locations
# (LangGraph versions may have it in different places)
try:
    from langgraph_service.graph.message import add_messages
except ImportError:
    try:
        from langgraph_service.prebuilt import add_messages
    except ImportError:
        try:
            from langchain_core.messages import add_messages
        except ImportError:
            # Fallback: define a simple add_messages function
            def add_messages(left: List[Dict], right: List[Dict]) -> List[Dict]:
                """Simple add_messages fallback."""
                return left + right if left else right


class GraphState(TypedDict):
    """
    State structure that flows through the LangGraph.
    
    This TypedDict defines all the data that will be passed between
    graph nodes. Each node can read from and update this state.
    
    Fields:
        messages: Conversation history (annotated for LangGraph message handling)
        query: Current user query string
        retrieved_docs: List of retrieved documents from ChromaDB
        context: Formatted context string from retrieved documents
        response: Generated response from the LLM
        metadata: Additional metadata about the processing
    """
    
    # Conversation history
    # Annotated with add_messages for LangGraph's message handling
    messages: Annotated[List[Dict[str, str]], add_messages]
    
    # Current query
    query: str
    
    # Retrieved documents from ChromaDB
    # Each document is a dict with: text, score, id, metadata (optional)
    retrieved_docs: List[Dict[str, Any]]
    
    # Formatted context string
    # This is the formatted version of retrieved_docs ready for the LLM
    context: str
    
    # Generated response from LLM
    response: str
    
    # Additional metadata
    # Contains classification info, confidence scores, errors, etc.
    metadata: Dict[str, Any]


def create_initial_state(query: str) -> GraphState:
    """
    Create an initial GraphState from a user query.
    
    Args:
        query: The user's query string
        
    Returns:
        GraphState with initial values
    """
    return GraphState(
        messages=[],
        query=query,
        retrieved_docs=[],
        context="",
        response="",
        metadata={}
    )


def create_state_from_dict(data: Dict[str, Any]) -> GraphState:
    """
    Create a GraphState from a dictionary.
    
    Useful for creating state from API requests or other sources.
    
    Args:
        data: Dictionary with state fields
        
    Returns:
        GraphState instance
    """
    return GraphState(
        messages=data.get("messages", []),
        query=data.get("query", ""),
        retrieved_docs=data.get("retrieved_docs", []),
        context=data.get("context", ""),
        response=data.get("response", ""),
        metadata=data.get("metadata", {})
    )


def state_to_dict(state: GraphState) -> Dict[str, Any]:
    """
    Convert a GraphState to a dictionary.
    
    Useful for serialization or API responses.
    
    Args:
        state: GraphState instance
        
    Returns:
        Dictionary representation of the state
    """
    return {
        "messages": state.get("messages", []),
        "query": state.get("query", ""),
        "retrieved_docs": state.get("retrieved_docs", []),
        "context": state.get("context", ""),
        "response": state.get("response", ""),
        "metadata": state.get("metadata", {})
    }

