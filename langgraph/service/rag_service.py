"""
RAG Service - High-level interface for RAG operations.

This service provides a clean, high-level API for using the RAG functionality.
It encapsulates the graph and provides simple methods for chat interactions.
"""

from typing import List, Dict, Any, Optional
from langgraph.graph.graph import RAGGraph


class RAGService:
    """
    High-level RAG service interface.
    
    This class provides a simple API for RAG operations, hiding
    the complexity of graph management and state handling.
    """
    
    def __init__(self):
        """Initialize the RAG service with a graph instance."""
        self.graph = RAGGraph()
        self.conversation_history: List[Dict[str, str]] = []
    
    def chat(self, query: str, reset_history: bool = False) -> Dict[str, Any]:
        """
        Chat with the RAG system.
        
        Args:
            query: User's question
            reset_history: Whether to reset conversation history
        
        Returns:
            Dictionary containing:
                - response: Generated response text
                - retrieved_docs: Retrieved documents
                - metadata: Additional metadata
        """
        if reset_history:
            self.conversation_history = []
        
        # Invoke graph
        result = self.graph.invoke(
            query=query,
            conversation_history=self.conversation_history
        )
        
        # Update conversation history
        self.conversation_history = result.get("messages", [])
        
        # Return simplified result
        return {
            "response": result.get("response", ""),
            "retrieved_docs": result.get("retrieved_docs", []),
            "context": result.get("context", ""),
            "metadata": result.get("metadata", {})
        }
    
    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = []
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Get the current conversation history.
        
        Returns:
            List of message dictionaries
        """
        return self.conversation_history.copy()
    
    def stream_chat(self, query: str, reset_history: bool = False):
        """
        Stream chat responses (for debugging/observability).
        
        Args:
            query: User's question
            reset_history: Whether to reset conversation history
        
        Yields:
            State updates as the graph executes
        """
        if reset_history:
            self.conversation_history = []
        
        for state_update in self.graph.stream(
            query=query,
            conversation_history=self.conversation_history
        ):
            yield state_update



