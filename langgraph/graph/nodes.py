"""
LangGraph Nodes Implementation.

Each node represents a step in the RAG pipeline.
"""

from typing import Dict, Any
from .state import GraphState
from .query_classifier import QueryClassifier, QueryType
import sys
from pathlib import Path

# Add langgraph to path for imports
langgraph_dir = Path(__file__).parent.parent
sys.path.insert(0, str(langgraph_dir.parent))

from langgraph.rag.retriever import ChromaDBRetriever
from langgraph.rag.context_formatter import format_context
from langgraph.rag.prompts import SYSTEM_PROMPT, build_rag_prompt
from langgraph.llm.ollama_chat import OllamaChatClient
from langgraph.config.settings import (
    RETRIEVAL_TOP_K,
    ENABLE_CONVERSATION_HISTORY,
    MAX_HISTORY_LENGTH,
)


# Initialize components (can be dependency injected later)
_retriever = None
_llm_client = None
_query_classifier = None


def _get_retriever() -> ChromaDBRetriever:
    """Get or create retriever instance."""
    global _retriever
    if _retriever is None:
        _retriever = ChromaDBRetriever()
    return _retriever


def _get_llm_client() -> OllamaChatClient:
    """Get or create LLM client instance."""
    global _llm_client
    if _llm_client is None:
        _llm_client = OllamaChatClient()
    return _llm_client


def _get_query_classifier() -> QueryClassifier:
    """Get or create query classifier instance."""
    global _query_classifier
    if _query_classifier is None:
        _query_classifier = QueryClassifier()
    return _query_classifier


def retrieve_node(state: GraphState) -> GraphState:
    """
    Retrieve relevant documents from ChromaDB.
    
    This node:
    1. Extracts the query from state
    2. Uses ChromaDBRetriever to find similar documents
    3. Updates state with retrieved documents
    
    Args:
        state: Current graph state
    
    Returns:
        Updated state with retrieved_docs populated
    """
    query = state.get("query", "")
    
    if not query:
        state["retrieved_docs"] = []
        state["metadata"] = state.get("metadata", {})
        state["metadata"]["error"] = "No query provided"
        return state
    
    try:
        retriever = _get_retriever()
        retrieved_docs = retriever.retrieve_relevant_docs(query, top_k=RETRIEVAL_TOP_K)
        
        state["retrieved_docs"] = retrieved_docs
        state["metadata"] = state.get("metadata", {})
        state["metadata"]["retrieval_count"] = len(retrieved_docs)
        
    except Exception as e:
        state["retrieved_docs"] = []
        state["metadata"] = state.get("metadata", {})
        state["metadata"]["error"] = f"Retrieval failed: {str(e)}"
    
    return state


def format_context_node(state: GraphState) -> GraphState:
    """
    Format retrieved documents into context string.
    
    This node:
    1. Takes retrieved documents from state
    2. Formats them into a context string
    3. Updates state with formatted context
    
    Args:
        state: Current graph state
    
    Returns:
        Updated state with context populated
    """
    retrieved_docs = state.get("retrieved_docs", [])
    
    try:
        context = format_context(retrieved_docs)
        state["context"] = context
        
    except Exception as e:
        state["context"] = "Error formatting context."
        state["metadata"] = state.get("metadata", {})
        state["metadata"]["format_error"] = str(e)
    
    return state


def generate_node(state: GraphState) -> GraphState:
    """
    Generate response using LLM.
    
    This node:
    1. Builds messages array with system prompt, context, and query
    2. Includes conversation history if enabled
    3. Calls LLM to generate response
    4. Updates state with generated response
    
    Args:
        state: Current graph state
    
    Returns:
        Updated state with response populated
    """
    query = state.get("query", "")
    context = state.get("context", "")
    messages = state.get("messages", [])
    
    if not query:
        state["response"] = "I didn't receive a query. Please try again."
        return state
    
    try:
        llm_client = _get_llm_client()
        
        # Build messages array
        llm_messages = []
        
        # Add system message
        llm_messages.append({
            "role": "system",
            "content": SYSTEM_PROMPT
        })
        
        # Add conversation history if enabled
        if ENABLE_CONVERSATION_HISTORY and messages:
            # Limit history length
            history = messages[-MAX_HISTORY_LENGTH * 2:] if len(messages) > MAX_HISTORY_LENGTH * 2 else messages
            llm_messages.extend(history)
        
        # Build RAG prompt with context and query
        user_content = build_rag_prompt(query, context, include_system=False)
        llm_messages.append({
            "role": "user",
            "content": user_content
        })
        
        # Generate response
        response = llm_client.generate_response(llm_messages)
        state["response"] = response
        
        state["metadata"] = state.get("metadata", {})
        state["metadata"]["generation_success"] = True
        
    except Exception as e:
        state["response"] = f"I encountered an error while generating a response: {str(e)}"
        state["metadata"] = state.get("metadata", {})
        state["metadata"]["generation_error"] = str(e)
    
    return state


def respond_node(state: GraphState) -> GraphState:
    """
    Finalize response and update conversation history.
    
    This node:
    1. Formats the final response
    2. Updates conversation history
    3. Returns final state
    
    Args:
        state: Current graph state
    
    Returns:
        Final state with updated messages
    """
    query = state.get("query", "")
    response = state.get("response", "")
    
    # Update conversation history
    # LangGraph's add_messages will handle this automatically via the Annotated type
    # But we can also manually add if needed
    if ENABLE_CONVERSATION_HISTORY:
        messages = state.get("messages", [])
        messages.append({"role": "user", "content": query})
        messages.append({"role": "assistant", "content": response})
        
        # Limit history length
        if len(messages) > MAX_HISTORY_LENGTH * 2:
            messages = messages[-MAX_HISTORY_LENGTH * 2:]
        
        state["messages"] = messages
    
    return state


def classify_query_node(state: GraphState) -> GraphState:
    """
    Classify the user query to determine routing strategy.
    
    This node:
    1. Analyzes the user query
    2. Determines if RAG is needed or direct answer is sufficient
    3. Updates state with classification metadata
    
    Args:
        state: Current graph state
    
    Returns:
        Updated state with query classification
    """
    query = state.get("query", "")
    
    if not query:
        state["metadata"] = state.get("metadata", {})
        state["metadata"]["query_type"] = "empty"
        state["metadata"]["classification_error"] = "No query provided"
        return state
    
    try:
        classifier = _get_query_classifier()
        query_type, confidence, classification_metadata = classifier.classify_query(query)
        
        # Update state metadata
        state["metadata"] = state.get("metadata", {})
        state["metadata"]["query_type"] = query_type.value
        state["metadata"]["classification_confidence"] = confidence
        state["metadata"]["classification_details"] = classification_metadata
        
    except Exception as e:
        state["metadata"] = state.get("metadata", {})
        state["metadata"]["query_type"] = "error"
        state["metadata"]["classification_error"] = str(e)
    
    return state


def direct_answer_node(state: GraphState) -> GraphState:
    """
    Generate direct answer without RAG retrieval.
    
    This node:
    1. Handles queries that don't require knowledge base lookup
    2. Uses LLM directly for general questions, greetings, etc.
    3. Updates state with generated response
    
    Args:
        state: Current graph state
    
    Returns:
        Updated state with direct response
    """
    query = state.get("query", "")
    messages = state.get("messages", [])
    query_type = state.get("metadata", {}).get("query_type", "unknown")
    
    if not query:
        state["response"] = "I didn't receive a query. Please try again."
        return state
    
    try:
        llm_client = _get_llm_client()
        
        # Build messages for direct answer
        llm_messages = []
        
        # Different system prompts based on query type
        if query_type == "greeting":
            system_prompt = """You are a friendly payment support assistant. 
            Respond to greetings warmly and offer to help with payment-related questions.
            Keep responses brief and welcoming."""
        
        elif query_type == "direct_answer":
            system_prompt = """You are a helpful assistant. 
            Answer general questions directly and concisely.
            If asked about payment-specific topics, suggest the user ask specific payment questions."""
        
        else:
            system_prompt = """You are a payment support assistant.
            Answer the question directly and helpfully.
            If you need specific payment information, let the user know you can help with payment-related questions."""
        
        llm_messages.append({
            "role": "system",
            "content": system_prompt
        })
        
        # Add conversation history if enabled
        if ENABLE_CONVERSATION_HISTORY and messages:
            history = messages[-MAX_HISTORY_LENGTH * 2:] if len(messages) > MAX_HISTORY_LENGTH * 2 else messages
            llm_messages.extend(history)
        
        # Add user query
        llm_messages.append({
            "role": "user",
            "content": query
        })
        
        # Generate response
        response = llm_client.generate_response(llm_messages)
        state["response"] = response
        
        state["metadata"] = state.get("metadata", {})
        state["metadata"]["generation_success"] = True
        state["metadata"]["response_type"] = "direct"
        
    except Exception as e:
        state["response"] = f"I encountered an error while generating a response: {str(e)}"
        state["metadata"] = state.get("metadata", {})
        state["metadata"]["generation_error"] = str(e)
        state["metadata"]["response_type"] = "error"
    
    return state

