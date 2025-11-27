"""
LangGraph Graph Definition and Compilation.

This module defines the graph structure and compiles it into an executable graph.
"""

from langgraph.graph import StateGraph
from .state import GraphState
from .nodes import (
    classify_query_node,
    retrieve_node,
    format_context_node,
    generate_node,
    direct_answer_node,
    respond_node,
)
from .query_classifier import QueryType


class RAGGraph:
    """
    RAG Graph wrapper class.
    
    This class encapsulates the compiled graph and provides
    a clean interface for interacting with it.
    """
    
    def __init__(self):
        """Initialize and compile the graph."""
        self.graph = self._create_graph()
        self.compiled_graph = self.graph.compile()
    
    def _create_graph(self) -> StateGraph:
        """
        Create and configure the LangGraph with intelligent routing.
        
        Returns:
            Configured StateGraph instance
        """
        graph = StateGraph(GraphState)
        
        # Add nodes
        graph.add_node("classify_query", classify_query_node)
        graph.add_node("retrieve", retrieve_node)
        graph.add_node("format_context", format_context_node)
        graph.add_node("generate", generate_node)
        graph.add_node("direct_answer", direct_answer_node)
        graph.add_node("respond", respond_node)
        
        # Define entry point
        graph.set_entry_point("classify_query")
        
        # Conditional routing based on query classification
        def route_after_classification(state: GraphState) -> str:
            """Route based on query classification."""
            query_type = state.get("metadata", {}).get("query_type", "rag_required")
            
            if query_type in ["greeting", "direct_answer"]:
                return "direct_answer"
            elif query_type in ["rag_required", "unclear"]:
                return "retrieve"
            else:
                # Default to RAG for unknown types
                return "retrieve"
        
        # Add conditional edge from classify_query
        graph.add_conditional_edges(
            "classify_query",
            route_after_classification,
            {
                "direct_answer": "direct_answer",
                "retrieve": "retrieve"
            }
        )
        
        # RAG path: retrieve -> format_context -> generate -> respond
        graph.add_edge("retrieve", "format_context")
        graph.add_edge("format_context", "generate")
        graph.add_edge("generate", "respond")
        
        # Direct answer path: direct_answer -> respond
        graph.add_edge("direct_answer", "respond")
        
        return graph
    
    def invoke(self, query: str, conversation_history: list = None) -> dict:
        """
        Invoke the graph with a query.
        
        Args:
            query: User query string
            conversation_history: Optional conversation history
        
        Returns:
            Final state dictionary
        """
        initial_state = {
            "messages": conversation_history or [],
            "query": query,
            "retrieved_docs": [],
            "context": "",
            "response": "",
            "metadata": {}
        }
        
        result = self.compiled_graph.invoke(initial_state)
        return result
    
    def stream(self, query: str, conversation_history: list = None):
        """
        Stream the graph execution (for debugging/observability).
        
        Args:
            query: User query string
            conversation_history: Optional conversation history
        
        Yields:
            State updates as the graph executes
        """
        initial_state = {
            "messages": conversation_history or [],
            "query": query,
            "retrieved_docs": [],
            "context": "",
            "response": "",
            "metadata": {}
        }
        
        for state_update in self.compiled_graph.stream(initial_state):
            yield state_update


def create_graph() -> RAGGraph:
    """
    Factory function to create a RAG graph instance.
    
    Returns:
        RAGGraph instance
    """
    return RAGGraph()



