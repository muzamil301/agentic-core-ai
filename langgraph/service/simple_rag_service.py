"""
Simplified RAG Service without complex graph dependencies.

This version avoids circular imports and complex LangGraph setup.
"""

from typing import List, Dict, Any, Optional
import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from db.chromadb_service import ChromaDBService
from utils import text_to_embeddings


class SimpleRAGService:
    """
    Simplified RAG service that works without complex graph setup.
    
    This provides the same functionality as the full RAG service but
    with simpler, more reliable implementation.
    """
    
    def __init__(self):
        """Initialize the simple RAG service."""
        self.conversation_history: List[Dict[str, str]] = []
        
        # Initialize components
        try:
            self.db_service = ChromaDBService(collection_name="payment_support")
            self.llm_client = self._init_llm_client()
            self.classifier = self._init_classifier()
            print("✅ Simple RAG service initialized successfully")
        except Exception as e:
            print(f"⚠️  RAG service initialization warning: {e}")
            self.db_service = None
            self.llm_client = None
            self.classifier = None
    
    def _init_llm_client(self):
        """Initialize LLM client."""
        try:
            from langgraph.llm.ollama_chat import OllamaChatClient
            return OllamaChatClient()
        except Exception as e:
            print(f"⚠️  LLM client initialization failed: {e}")
            return None
    
    def _init_classifier(self):
        """Initialize query classifier."""
        try:
            from langgraph.graph.query_classifier import QueryClassifier
            return QueryClassifier()
        except Exception as e:
            print(f"⚠️  Classifier initialization failed: {e}")
            return None
    
    def _classify_query(self, query: str) -> str:
        """Classify the query type."""
        if not self.classifier:
            return "rag_required"  # Default to RAG
        
        try:
            query_type, confidence, metadata = self.classifier.classify_query(query)
            return query_type.value
        except Exception:
            return "rag_required"
    
    def _retrieve_documents(self, query: str, top_k: int = 3) -> List[Dict]:
        """Retrieve relevant documents."""
        if not self.db_service:
            return []
        
        try:
            results = self.db_service.read(
                query_texts=[query],
                n_results=top_k
            )
            
            retrieved_docs = []
            if results.get('ids') and len(results['ids']) > 0:
                ids = results['ids'][0]
                documents = results['documents'][0]
                metadatas = results.get('metadatas', [[]])[0] if results.get('metadatas') else [{}] * len(ids)
                distances = results.get('distances', [[]])[0] if results.get('distances') else [1.0] * len(ids)
                
                for doc_id, doc_text, metadata, distance in zip(ids, documents, metadatas, distances):
                    retrieved_docs.append({
                        "id": doc_id,
                        "text": doc_text,
                        "metadata": metadata if metadata else {},
                        "distance": distance
                    })
            
            return retrieved_docs
        except Exception as e:
            print(f"⚠️  Document retrieval failed: {e}")
            return []
    
    def _format_context(self, retrieved_docs: List[Dict]) -> str:
        """Format retrieved documents into context."""
        if not retrieved_docs:
            return "No relevant context found."
        
        context_parts = []
        for i, doc in enumerate(retrieved_docs, 1):
            text = doc.get("text", "")
            metadata = doc.get("metadata", {})
            
            entry = f"[{i}]"
            if metadata.get("category"):
                entry += f" Category: {metadata['category']}"
            entry += f" {text}"
            
            context_parts.append(entry)
        
        return "\n\n".join(context_parts)
    
    def _generate_response(self, query: str, context: str = "", query_type: str = "rag_required") -> str:
        """Generate response using LLM."""
        if not self.llm_client:
            return "I'm sorry, the chat service is currently unavailable. Please check that Ollama is running with a chat model."
        
        try:
            # Build messages
            messages = []
            
            # System prompt based on query type
            if query_type == "greeting":
                system_prompt = "You are a friendly payment support assistant. Respond to greetings warmly and offer to help with payment-related questions."
            elif query_type == "direct_answer":
                system_prompt = "You are a helpful assistant. Answer general questions directly and concisely."
            else:
                system_prompt = "You are a helpful payment support assistant. Answer questions based on the provided context. If the context doesn't contain the answer, say you don't have that information."
            
            messages.append({"role": "system", "content": system_prompt})
            
            # Add conversation history
            if self.conversation_history:
                messages.extend(self.conversation_history[-10:])  # Last 10 messages
            
            # Add current query with context if available
            if context and query_type == "rag_required":
                user_content = f"Context from knowledge base:\n{context}\n\nQuestion: {query}"
            else:
                user_content = query
            
            messages.append({"role": "user", "content": user_content})
            
            # Generate response
            response = self.llm_client.generate_response(messages)
            return response
            
        except Exception as e:
            return f"I encountered an error while generating a response: {str(e)}"
    
    def chat(self, query: str, reset_history: bool = False) -> Dict[str, Any]:
        """
        Chat with the RAG system.
        
        Args:
            query: User's question
            reset_history: Whether to reset conversation history
        
        Returns:
            Dictionary containing response and metadata
        """
        if reset_history:
            self.conversation_history = []
        
        # Classify query
        query_type = self._classify_query(query)
        
        # Retrieve documents if needed
        retrieved_docs = []
        context = ""
        if query_type == "rag_required":
            retrieved_docs = self._retrieve_documents(query)
            context = self._format_context(retrieved_docs)
        
        # Generate response
        response = self._generate_response(query, context, query_type)
        
        # Update conversation history
        self.conversation_history.append({"role": "user", "content": query})
        self.conversation_history.append({"role": "assistant", "content": response})
        
        # Prepare metadata
        metadata = {
            "query_type": query_type,
            "retrieval_count": len(retrieved_docs),
            "response_type": "rag" if retrieved_docs else "direct",
            "service_type": "simple_rag"
        }
        
        return {
            "response": response,
            "retrieved_docs": retrieved_docs,
            "context": context,
            "metadata": metadata
        }
    
    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = []
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the current conversation history."""
        return self.conversation_history.copy()
