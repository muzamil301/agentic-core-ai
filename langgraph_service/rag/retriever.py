"""
ChromaDB Retriever for LangGraph RAG Service

This module provides document retrieval functionality from ChromaDB
using semantic similarity search.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add project root to path to import from db and utils
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from db.chromadb_service import ChromaDBService
from utils import text_to_embeddings
from langgraph_service.config import (
    CHROMADB_PERSIST_DIRECTORY,
    COLLECTION_NAME,
    OLLAMA_EMBED_API_URL,
    EMBEDDING_MODEL,
    OLLAMA_TIMEOUT,
    RETRIEVAL_TOP_K,
    SIMILARITY_THRESHOLD,
)


class ChromaDBRetriever:
    """
    Retrieves relevant documents from ChromaDB using semantic similarity.
    
    This class:
    1. Converts user queries to embeddings using Ollama
    2. Searches ChromaDB for similar documents
    3. Returns top-k relevant documents with similarity scores
    """
    
    def __init__(
        self,
        collection_name: str = COLLECTION_NAME,
        persist_directory: str = CHROMADB_PERSIST_DIRECTORY,
        embedding_model: str = EMBEDDING_MODEL,
        embed_api_url: str = OLLAMA_EMBED_API_URL,
        timeout: int = OLLAMA_TIMEOUT,
    ):
        """
        Initialize the ChromaDB retriever.
        
        Args:
            collection_name: Name of the ChromaDB collection
            persist_directory: Directory where ChromaDB data is stored
            embedding_model: Model name for generating embeddings
            embed_api_url: Ollama embeddings API URL
            timeout: Request timeout in seconds
        """
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        self.embed_api_url = embed_api_url
        self.timeout = timeout
        
        # Initialize ChromaDB service
        self.chromadb_service = ChromaDBService(
            collection_name=collection_name,
            persist_directory=persist_directory,
            create_collection=True
        )
    
    def retrieve_relevant_docs(
        self,
        query: str,
        top_k: int = RETRIEVAL_TOP_K,
        similarity_threshold: float = SIMILARITY_THRESHOLD,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a given query.
        
        Args:
            query: The user's query string
            top_k: Number of documents to retrieve (default from config)
            similarity_threshold: Minimum similarity score (0.0 to 1.0)
            
        Returns:
            List of dictionaries, each containing:
                - text: Document text
                - score: Similarity score (higher is more similar)
                - metadata: Document metadata (if available)
                - id: Document ID (if available)
                
        Raises:
            ValueError: If query is empty
            ConnectionError: If Ollama API is unavailable
        """
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")
        
        # Convert query to embedding
        query_embedding = self._query_to_embedding(query)
        
        # Search ChromaDB
        results = self.chromadb_service.read(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Format results
        formatted_results = self._format_results(
            results,
            similarity_threshold=similarity_threshold
        )
        
        return formatted_results
    
    def _query_to_embedding(self, query: str) -> List[float]:
        """
        Convert a query string to an embedding vector.
        
        Args:
            query: The query string
            
        Returns:
            List of floats representing the embedding vector
            
        Raises:
            ConnectionError: If Ollama API is unavailable
        """
        try:
            embeddings = text_to_embeddings(
                texts=[query],
                model=self.embedding_model,
                api_url=self.embed_api_url
            )
            
            if not embeddings or len(embeddings) == 0:
                raise ConnectionError("No embeddings returned from Ollama API")
            
            return embeddings[0]
            
        except Exception as e:
            raise ConnectionError(
                f"Failed to generate embedding for query: {e}. "
                f"Please ensure Ollama is running and the model '{self.embedding_model}' is available."
            )
    
    def _format_results(
        self,
        results: Dict[str, Any],
        similarity_threshold: float = SIMILARITY_THRESHOLD
    ) -> List[Dict[str, Any]]:
        """
        Format ChromaDB query results into a standardized format.
        
        Args:
            results: Raw results from ChromaDB query
            similarity_threshold: Minimum similarity score to include
            
        Returns:
            List of formatted document dictionaries
        """
        formatted = []
        
        # Check if results are empty
        if not results or not results.get("ids") or len(results["ids"]) == 0:
            return formatted
        
        # Extract data from results
        ids = results.get("ids", [])
        documents = results.get("documents", [])
        distances = results.get("distances", [])
        metadatas = results.get("metadatas", [])
        
        # ChromaDB returns lists of lists (one list per query)
        # Since we query with one embedding, we get the first list
        if ids and isinstance(ids[0], list):
            ids = ids[0]
            documents = documents[0] if documents else []
            distances = distances[0] if distances else []
            metadatas = metadatas[0] if metadatas else []
        
        # Format each result
        for i in range(len(ids)):
            # Convert distance to similarity score
            # ChromaDB uses cosine distance (0 = identical, 1 = opposite)
            # We convert to similarity (1 = identical, 0 = opposite)
            distance = distances[i] if i < len(distances) else 1.0
            similarity_score = 1.0 - distance
            
            # Filter by similarity threshold
            if similarity_score < similarity_threshold:
                continue
            
            # Build result dictionary
            result_dict = {
                "text": documents[i] if i < len(documents) else "",
                "score": similarity_score,
                "id": ids[i] if i < len(ids) else None,
            }
            
            # Add metadata if available
            if metadatas and i < len(metadatas) and metadatas[i]:
                result_dict["metadata"] = metadatas[i]
            
            formatted.append(result_dict)
        
        # Sort by score (highest first)
        formatted.sort(key=lambda x: x["score"], reverse=True)
        
        return formatted
    
    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the ChromaDB collection.
        
        Returns:
            Dictionary with collection information
        """
        return self.chromadb_service.get_info()


def retrieve_documents(
    query: str,
    top_k: int = RETRIEVAL_TOP_K,
    similarity_threshold: float = SIMILARITY_THRESHOLD,
) -> List[Dict[str, Any]]:
    """
    Convenience function to retrieve documents for a query.
    
    Args:
        query: The user's query string
        top_k: Number of documents to retrieve
        similarity_threshold: Minimum similarity score
        
    Returns:
        List of formatted document dictionaries
    """
    retriever = ChromaDBRetriever()
    return retriever.retrieve_relevant_docs(
        query=query,
        top_k=top_k,
        similarity_threshold=similarity_threshold,
    )

