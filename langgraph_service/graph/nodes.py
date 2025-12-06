"""
LangGraph Node Functions

This module contains all the node functions that process the GraphState.
Each node function takes state as input, processes it, and returns updated state.
"""

from typing import Dict, Any
from langgraph_service.graph.state import GraphState
from langgraph_service.graph.query_classifier import QueryClassifier, QueryType
from langgraph_service.rag.retriever import ChromaDBRetriever
from langgraph_service.llm.ollama_chat import OllamaChatClient
from langgraph_service.config import (
    RETRIEVAL_TOP_K,
    SIMILARITY_THRESHOLD,
    MAX_CONTEXT_LENGTH,
)


def format_context(documents: list, max_length: int = MAX_CONTEXT_LENGTH) -> str:
    """
    Format retrieved documents into a context string for the LLM.
    
    Args:
        documents: List of document dictionaries with 'text', 'score', etc.
        max_length: Maximum length of the formatted context
        
    Returns:
        Formatted context string
    """
    if not documents:
        return ""
    
    context_parts = []
    current_length = 0
    
    for i, doc in enumerate(documents, 1):
        text = doc.get("text", "")
        score = doc.get("score", 0)
        
        # Format: "Document 1 (relevance: 0.85): ..."
        doc_text = f"Document {i} (relevance: {score:.2f}): {text}"
        
        # Check if adding this document would exceed max length
        if current_length + len(doc_text) > max_length:
            # Truncate this document if needed
            remaining = max_length - current_length - 50  # Reserve space for formatting
            if remaining > 0:
                doc_text = f"Document {i} (relevance: {score:.2f}): {text[:remaining]}..."
            else:
                break
        
        context_parts.append(doc_text)
        current_length += len(doc_text)
    
    return "\n\n".join(context_parts)


def classify_query_node(state: GraphState) -> Dict[str, Any]:
    """
    Node: Classify the user query.
    
    This node classifies the query to determine the appropriate response strategy.
    Updates the metadata field with classification results.
    
    Args:
        state: Current graph state
        
    Returns:
        Dictionary with updated metadata
    """
    query = state.get("query", "")
    
    if not query:
        return {
            "metadata": {
                **state.get("metadata", {}),
                "query_type": "unclear",
                "classification_error": "Empty query"
            }
        }
    
    # Classify query
    classifier = QueryClassifier()
    query_type, confidence, classification_metadata = classifier.classify_query(query)
    
    # Update metadata
    updated_metadata = {
        **state.get("metadata", {}),
        "query_type": query_type.value,
        "classification_confidence": confidence,
        "classification_metadata": classification_metadata
    }
    
    return {
        "metadata": updated_metadata
    }


def retrieve_node(state: GraphState) -> Dict[str, Any]:
    """
    Node: Retrieve relevant documents from ChromaDB.
    
    This node retrieves documents based on the query using semantic similarity.
    Updates the retrieved_docs field.
    
    Args:
        state: Current graph state
        
    Returns:
        Dictionary with updated retrieved_docs
    """
    query = state.get("query", "")
    
    if not query:
        return {
            "retrieved_docs": []
        }
    
    # Retrieve documents
    retriever = ChromaDBRetriever()
    try:
        retrieved_docs = retriever.retrieve_relevant_docs(
            query=query,
            top_k=RETRIEVAL_TOP_K,
            similarity_threshold=SIMILARITY_THRESHOLD
        )
    except Exception as e:
        # Update metadata with error
        metadata = state.get("metadata", {})
        metadata["retrieval_error"] = str(e)
        
        return {
            "retrieved_docs": [],
            "metadata": metadata
        }
    
    return {
        "retrieved_docs": retrieved_docs
    }


def format_context_node(state: GraphState) -> Dict[str, Any]:
    """
    Node: Format retrieved documents into context string.
    
    This node formats the retrieved documents into a context string
    that will be used by the LLM. Updates the context field.
    
    Args:
        state: Current graph state
        
    Returns:
        Dictionary with updated context
    """
    retrieved_docs = state.get("retrieved_docs", [])
    
    # Format context
    context = format_context(retrieved_docs, max_length=MAX_CONTEXT_LENGTH)
    
    # Update metadata
    metadata = state.get("metadata", {})
    metadata["context_length"] = len(context)
    metadata["docs_count"] = len(retrieved_docs)
    
    return {
        "context": context,
        "metadata": metadata
    }


def generate_node(state: GraphState) -> Dict[str, Any]:
    """
    Node: Generate response using LLM with RAG context.
    
    This node generates a response using the LLM with the formatted context.
    Updates the response field.
    
    Args:
        state: Current graph state
        
    Returns:
        Dictionary with updated response
    """

    # print("state here generate_node", state.get("context", ""));
    # print("state here generate_node", state.get("query", ""));
    # print("state here generate_node", state.get("messages", ""));
    # print("state here generate_node", state.get("retrieved_docs", ""));
    # print("state here generate_node", state.get("metadata", ""));
    # print("state here generate_node", state.get("response", ""));
    # print("state here generate_node", state.get("generation_error", ""));
    # print("state here generate_node", state.get("generation_error", ""));
    query = state.get("query", "")
    context = state.get("context", "")
    messages_history = state.get("messages", [])
    
    if not query:
        return {
            "response": "I didn't receive a valid query. Please try again."
        }
    
    # Create RAG prompt
    system_prompt = (
        "You are a helpful customer support assistant. "
        "Use the provided context from the knowledge base to answer questions accurately. "
        "If the context doesn't contain relevant information, say so. "
        "Be concise and helpful."
    )
    
    user_message = f"""Context from knowledge base:
{context}

Question: {query}

Please provide a helpful answer based on the context above."""
    
    # Build messages (include history if available)
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    # Add conversation history
    messages.extend(messages_history)
    
    # Add current query
    messages.append({"role": "user", "content": user_message})
    
    # Generate response
    llm_client = OllamaChatClient()
    try:
        response = llm_client.generate_response(messages)
    except Exception as e:
        # Update metadata with error
        metadata = state.get("metadata", {})
        metadata["generation_error"] = str(e)
        
        return {
            "response": f"I encountered an error while generating a response: {str(e)}",
            "metadata": metadata
        }
    
    return {
        "response": response
    }


def direct_answer_node(state: GraphState) -> Dict[str, Any]:
    """
    Node: Generate direct answer without RAG context.
    
    This node generates a response directly from the LLM without
    using retrieved documents. Updates the response field.
    
    Args:
        state: Current graph state
        
    Returns:
        Dictionary with updated response
    """
    query = state.get("query", "")
    messages_history = state.get("messages", [])
    
    if not query:
        return {
            "response": "I didn't receive a valid query. Please try again."
        }
    
    # Create direct answer prompt
    system_prompt = (
        "You are a helpful assistant. "
        "Answer questions directly and helpfully."
    )
    
    # Build messages
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    # Add conversation history
    messages.extend(messages_history)
    
    # Add current query
    messages.append({"role": "user", "content": query})
    
    # Generate response
    llm_client = OllamaChatClient()
    try:
        response = llm_client.generate_response(messages)
    except Exception as e:
        # Update metadata with error
        metadata = state.get("metadata", {})
        metadata["generation_error"] = str(e)
        
        return {
            "response": f"I encountered an error while generating a response: {str(e)}",
            "metadata": metadata
        }
    
    return {
        "response": response
    }


def respond_node(state: GraphState) -> Dict[str, Any]:
    """
    Node: Final response formatting and message history update.
    
    This node formats the final response and updates the message history.
    This is typically the last node in the pipeline.
    
    Args:
        state: Current graph state
        
    Returns:
        Dictionary with updated messages
    """
    query = state.get("query", "")
    response = state.get("response", "")
    current_messages = state.get("messages", [])
    
    # Add user message to history
    updated_messages = current_messages.copy()
    if query:
        updated_messages.append({"role": "user", "content": query})
    
    # Add assistant response to history
    if response:
        updated_messages.append({"role": "assistant", "content": response})
    
    # Update metadata
    metadata = state.get("metadata", {})
    metadata["response_length"] = len(response)
    
    return {
        "messages": updated_messages,
        "metadata": metadata
    }

