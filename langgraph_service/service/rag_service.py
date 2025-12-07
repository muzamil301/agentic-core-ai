"""
High-level RAG Service

This module provides a clean, user-friendly interface for the RAG system.
It wraps the LangGraph and manages conversation history, state initialization,
and provides both synchronous and streaming interfaces.
"""

from typing import List, Dict, Any, Optional, Iterator
from langgraph_service.graph.graph import RAGGraph
from langgraph_service.graph.state import (
    GraphState,
    create_initial_state,
    state_to_dict,
)


class RAGService:
    """
    High-level service interface for the RAG system.
    
    This class provides a simple API for interacting with the RAG system,
    managing conversation history, and handling state initialization.
    
    Example:
        ```python
        service = RAGService()
        
        # Simple chat
        response = service.chat("What is my daily transaction limit?")
        print(response)
        
        # With conversation history
        service.chat("Hello")
        response = service.chat("What is my daily transaction limit?")
        
        # Streaming
        for update in service.stream("Tell me about cards"):
            print(update)
        ```
    """
    
    def __init__(self, enable_history: bool = True):
        """
        Initialize the RAG service.
        
        Args:
            enable_history: Whether to maintain conversation history.
                          If True, previous messages are included in context.
        """
        self.graph = RAGGraph()
        self.enable_history = enable_history
        self.conversation_history: List[Dict[str, str]] = []
    
    def chat(
        self,
        query: str,
        reset_history: bool = False,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Process a user query and return a response.
        
        This is the main method for interacting with the RAG system.
        It handles state initialization, graph execution, and response extraction.
        
        Args:
            query: The user's query string
            reset_history: If True, clears conversation history before processing
            system_prompt: Optional system prompt to override default behavior
            
        Returns:
            The generated response string
            
        Example:
            ```python
            service = RAGService()
            response = service.chat("What is my daily transaction limit?")
            print(response)
            ```
        """
        if reset_history:
            self.conversation_history = []
        
        # Create initial state
        state = create_initial_state(query)
        
        # Add conversation history if enabled
        if self.enable_history and self.conversation_history:
            state["messages"] = self.conversation_history.copy()
        
        # Add system prompt if provided
        if system_prompt:
            state["metadata"]["system_prompt"] = system_prompt
        
        # Execute the graph
        try:
            final_state = self.graph.invoke(state)
        except Exception as e:
            # Return error message
            error_msg = f"I encountered an error while processing your query: {str(e)}"
            if self.enable_history:
                self.conversation_history.append({"role": "user", "content": query})
                self.conversation_history.append({"role": "assistant", "content": error_msg})
            return error_msg
        
        # Extract response
        response = final_state.get("response", "")
        
        # Update conversation history
        if self.enable_history:
            self.conversation_history.append({"role": "user", "content": query})
            self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def stream(
        self,
        query: str,
        reset_history: bool = False,
        system_prompt: Optional[str] = None
    ) -> Iterator[Dict[str, Any]]:
        """
        Process a user query and stream intermediate results.
        
        This method yields state updates after each node execution,
        allowing you to see the progress of the RAG pipeline.
        
        Args:
            query: The user's query string
            reset_history: If True, clears conversation history before processing
            system_prompt: Optional system prompt to override default behavior
            
        Yields:
            Dictionary with node name and state update
            
        Example:
            ```python
            service = RAGService()
            for update in service.stream("What is my daily transaction limit?"):
                node_name = list(update.keys())[0]
                print(f"Node: {node_name}")
                print(f"State: {update[node_name]}")
            ```
        """
        if reset_history:
            self.conversation_history = []
        
        # Create initial state
        state = create_initial_state(query)
        
        # Add conversation history if enabled
        if self.enable_history and self.conversation_history:
            state["messages"] = self.conversation_history.copy()
        
        # Add system prompt if provided
        if system_prompt:
            state["metadata"]["system_prompt"] = system_prompt
        
        # Stream graph execution
        try:
            for state_update in self.graph.stream(state):
                yield state_update
                
                # Extract final state from last update
                if isinstance(state_update, dict):
                    for node_name, node_state in state_update.items():
                        if node_name == "respond":
                            # This is the final node
                            response = node_state.get("response", "")
                            if self.enable_history and response:
                                self.conversation_history.append({"role": "user", "content": query})
                                self.conversation_history.append({"role": "assistant", "content": response})
        except Exception as e:
            error_msg = f"I encountered an error while processing your query: {str(e)}"
            yield {"error": {"error": str(e), "message": error_msg}}
            if self.enable_history:
                self.conversation_history.append({"role": "user", "content": query})
                self.conversation_history.append({"role": "assistant", "content": error_msg})
    
    def get_history(self) -> List[Dict[str, str]]:
        """
        Get the conversation history.
        
        Returns:
            List of message dictionaries with 'role' and 'content' keys
        """
        return self.conversation_history.copy()
    
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
    
    def get_state_dict(self, query: str) -> Dict[str, Any]:
        """
        Get the state dictionary for a query without executing the graph.
        
        Useful for debugging or inspecting what state would be created.
        
        Args:
            query: The user's query string
            
        Returns:
            Dictionary representation of the initial state
        """
        state = create_initial_state(query)
        if self.enable_history and self.conversation_history:
            state["messages"] = self.conversation_history.copy()
        return state_to_dict(state)
    
    def invoke_with_state(self, state: GraphState) -> GraphState:
        """
        Invoke the graph with a custom state.
        
        This is a lower-level method for advanced use cases where you
        need full control over the state.
        
        Args:
            state: Custom GraphState to use
            
        Returns:
            Final GraphState after execution
        """
        return self.graph.invoke(state)

