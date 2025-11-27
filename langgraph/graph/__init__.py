"""
LangGraph graph definition and compilation.

This module contains:
- State: GraphState schema definition
- Nodes: Individual graph nodes (functions)
- Graph: Graph definition and compilation
"""

"""
LangGraph graph definition and compilation.

This module contains the graph components for the RAG system.
"""

# Import order matters to avoid circular imports
from .query_classifier import QueryClassifier, QueryType
from .state import GraphState

# Import nodes and graph after state is defined
def get_nodes():
    """Lazy import of nodes to avoid circular imports."""
    from .nodes import (
        classify_query_node,
        retrieve_node,
        format_context_node,
        generate_node,
        direct_answer_node,
        respond_node,
    )
    return {
        "classify_query_node": classify_query_node,
        "retrieve_node": retrieve_node,
        "format_context_node": format_context_node,
        "generate_node": generate_node,
        "direct_answer_node": direct_answer_node,
        "respond_node": respond_node,
    }

def get_graph_classes():
    """Lazy import of graph classes to avoid circular imports."""
    from .graph import create_graph, RAGGraph
    return create_graph, RAGGraph

__all__ = [
    "GraphState",
    "QueryClassifier", 
    "QueryType",
    "get_nodes",
    "get_graph_classes",
]



