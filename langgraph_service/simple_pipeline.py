"""
Simple Linear RAG Pipeline

This module provides a simple, linear implementation of the RAG pipeline
without using LangGraph. It combines all components in sequence to demonstrate
the complete flow.

This is useful for:
- Understanding how RAG works end-to-end
- Testing components together
- Debugging the pipeline
- Learning before moving to LangGraph
"""

from typing import Dict, Any, List, Optional
from langgraph_service.graph.query_classifier import QueryClassifier, QueryType
from langgraph_service.rag.retriever import ChromaDBRetriever
from langgraph_service.llm.ollama_chat import OllamaChatClient
from langgraph_service.config import (
    RETRIEVAL_TOP_K,
    SIMILARITY_THRESHOLD,
    MAX_CONTEXT_LENGTH,
)


def format_context(documents: List[Dict[str, Any]], max_length: int = MAX_CONTEXT_LENGTH) -> str:
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


def create_rag_prompt(query: str, context: str) -> List[Dict[str, str]]:
    """
    Create a prompt for RAG-based response generation.
    
    Args:
        query: The user's query
        context: Formatted context from retrieved documents
        
    Returns:
        List of messages for the LLM
    """
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
    
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]


def create_direct_answer_prompt(query: str) -> List[Dict[str, str]]:
    """
    Create a prompt for direct answer (no RAG context).
    
    Args:
        query: The user's query
        
    Returns:
        List of messages for the LLM
    """
    system_prompt = (
        "You are a helpful assistant. "
        "Answer questions directly and helpfully."
    )
    
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]


def process_query(
    query: str,
    top_k: int = RETRIEVAL_TOP_K,
    similarity_threshold: float = SIMILARITY_THRESHOLD,
) -> Dict[str, Any]:
    """
    Process a query through the complete RAG pipeline.
    
    This is the main function that combines all components:
    1. Classify query
    2. Retrieve documents (if RAG needed)
    3. Format context
    4. Generate response
    
    Args:
        query: The user's query string
        top_k: Number of documents to retrieve
        similarity_threshold: Minimum similarity score for documents
        
    Returns:
        Dictionary containing:
            - response: Generated response text
            - query_type: Type of query (rag_required, direct_answer, etc.)
            - retrieved_docs: List of retrieved documents (if any)
            - context: Formatted context string (if any)
            - metadata: Additional information about the processing
    """
    if not query or not query.strip():
        return {
            "response": "I didn't receive a valid query. Please try again.",
            "query_type": "unclear",
            "retrieved_docs": [],
            "context": "",
            "metadata": {
                "error": "empty_query"
            }
        }
    
    # Step 1: Classify query
    classifier = QueryClassifier()
    query_type, confidence, classification_metadata = classifier.classify_query(query)
    
    metadata = {
        "query_type": query_type.value,
        "classification_confidence": confidence,
        "classification_metadata": classification_metadata
    }
    
    # Step 2: Route based on classification
    if query_type == QueryType.GREETING:
        # Simple greeting response
        greeting_responses = {
            "hello": "Hello! How can I help you today?",
            "hi": "Hi there! What can I do for you?",
            "thanks": "You're welcome! Is there anything else I can help with?",
            "bye": "Goodbye! Have a great day!",
        }
        
        query_lower = query.lower()
        response = "Hello! How can I help you today?"
        for greeting, reply in greeting_responses.items():
            if greeting in query_lower:
                response = reply
                break
        
        return {
            "response": response,
            "query_type": query_type.value,
            "retrieved_docs": [],
            "context": "",
            "metadata": metadata
        }
    
    elif query_type == QueryType.UNCLEAR:
        # Unclear query - ask for clarification
        return {
            "response": "I'm not sure I understand your question. Could you please rephrase it or provide more details?",
            "query_type": query_type.value,
            "retrieved_docs": [],
            "context": "",
            "metadata": metadata
        }
    
    elif query_type == QueryType.RAG_REQUIRED:
        # RAG path: Retrieve → Format → Generate
        
        # Step 2a: Retrieve documents
        retriever = ChromaDBRetriever()
        try:
            retrieved_docs = retriever.retrieve_relevant_docs(
                query=query,
                top_k=top_k,
                similarity_threshold=similarity_threshold
            )
        except Exception as e:
            return {
                "response": f"I encountered an error while searching the knowledge base: {str(e)}",
                "query_type": query_type.value,
                "retrieved_docs": [],
                "context": "",
                "metadata": {
                    **metadata,
                    "error": str(e)
                }
            }
        
        # Step 2b: Format context
        context = format_context(retrieved_docs, max_length=MAX_CONTEXT_LENGTH)
        
        # Step 2c: Generate response with context
        llm_client = OllamaChatClient()
        try:
            messages = create_rag_prompt(query, context)
            response = llm_client.generate_response(messages)
        except Exception as e:
            return {
                "response": f"I encountered an error while generating a response: {str(e)}",
                "query_type": query_type.value,
                "retrieved_docs": retrieved_docs,
                "context": context,
                "metadata": {
                    **metadata,
                    "error": str(e)
                }
            }
        
        return {
            "response": response,
            "query_type": query_type.value,
            "retrieved_docs": retrieved_docs,
            "context": context,
            "metadata": {
                **metadata,
                "docs_retrieved": len(retrieved_docs),
                "context_length": len(context)
            }
        }
    
    else:  # DIRECT_ANSWER
        # Direct answer path: Generate without retrieval
        
        llm_client = OllamaChatClient()
        try:
            messages = create_direct_answer_prompt(query)
            response = llm_client.generate_response(messages)
        except Exception as e:
            return {
                "response": f"I encountered an error while generating a response: {str(e)}",
                "query_type": query_type.value,
                "retrieved_docs": [],
                "context": "",
                "metadata": {
                    **metadata,
                    "error": str(e)
                }
            }
        
        return {
            "response": response,
            "query_type": query_type.value,
            "retrieved_docs": [],
            "context": "",
            "metadata": metadata
        }


class SimpleRAGPipeline:
    """
    Simple RAG Pipeline class for easier usage.
    
    This class wraps the process_query function and provides
    a cleaner interface for multiple queries.
    """
    
    def __init__(
        self,
        top_k: int = RETRIEVAL_TOP_K,
        similarity_threshold: float = SIMILARITY_THRESHOLD,
    ):
        """
        Initialize the pipeline.
        
        Args:
            top_k: Number of documents to retrieve
            similarity_threshold: Minimum similarity score
        """
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold
    
    def process(self, query: str) -> Dict[str, Any]:
        """
        Process a query through the pipeline.
        
        Args:
            query: The user's query string
            
        Returns:
            Dictionary with response and metadata
        """
        return process_query(
            query=query,
            top_k=self.top_k,
            similarity_threshold=self.similarity_threshold
        )


def chat(query: str) -> str:
    """
    Convenience function for simple chat interactions.
    
    Args:
        query: The user's query string
        
    Returns:
        Response string
    """
    result = process_query(query)
    return result.get("response", "I'm sorry, I couldn't generate a response.")


if __name__ == "__main__":
    # Simple CLI interface for testing
    import sys
    
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        result = process_query(query)
        print("\n" + "=" * 70)
        print(f"Query: {query}")
        print("-" * 70)
        print(f"Type: {result['query_type']}")
        print(f"Response: {result['response']}")
        if result.get('retrieved_docs'):
            print(f"\nRetrieved {len(result['retrieved_docs'])} documents")
        print("=" * 70)
    else:
        print("Usage: python simple_pipeline.py 'Your query here'")

