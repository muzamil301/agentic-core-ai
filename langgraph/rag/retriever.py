"""
ChromaDB Retriever for RAG.

This module provides a clean interface for retrieving relevant documents
from ChromaDB using semantic search.
"""

from typing import List, Dict, Any, Optional
import sys
from pathlib import Path

# Add parent directory to path to import existing modules
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from db.chromadb_service import ChromaDBService
from utils import text_to_embeddings
from langgraph.config.settings import (
    RETRIEVAL_TOP_K,
    SIMILARITY_THRESHOLD,
    COLLECTION_NAME,
    CHROMADB_PERSIST_DIRECTORY,
)


class ChromaDBRetriever:
    """
    Retriever for querying ChromaDB and retrieving relevant documents.
    
    This class wraps the existing ChromaDBService to provide a clean
    interface for RAG retrieval operations.
    """
    
    def __init__(
        self,
        collection_name: str = COLLECTION_NAME,
        persist_directory: str = CHROMADB_PERSIST_DIRECTORY,
        top_k: int = RETRIEVAL_TOP_K,
        similarity_threshold: float = SIMILARITY_THRESHOLD
    ):
        """
        Initialize the retriever.
        
        Args:
            collection_name: Name of the ChromaDB collection
            persist_directory: Directory where ChromaDB persists data
            top_k: Number of documents to retrieve
            similarity_threshold: Minimum similarity score (0.0 = no filter)
        """
        self.collection_name = collection_name
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold
        self.db_service = ChromaDBService(
            collection_name=collection_name,
            persist_directory=persist_directory
        )
    
    def retrieve_relevant_docs(self, query: str, top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a given query.
        
        Args:
            query: User query string
            top_k: Number of documents to retrieve (overrides default)
        
        Returns:
            List of dictionaries containing:
                - text: Document text
                - metadata: Document metadata
                - score: Similarity score (distance, lower is better)
                - id: Document ID
        """
        if top_k is None:
            top_k = self.top_k
        
        # Use existing ChromaDBService to query
        results = self.db_service.read(
            query_texts=[query],
            n_results=top_k
        )
        
        # Format results
        retrieved_docs = []
        
        if results.get('ids') and len(results['ids']) > 0:
            ids = results['ids'][0]
            documents = results['documents'][0]
            metadatas = results.get('metadatas', [[]])[0] if results.get('metadatas') else [{}] * len(ids)
            distances = results.get('distances', [[]])[0] if results.get('distances') else [1.0] * len(ids)
            
            for doc_id, doc_text, metadata, distance in zip(ids, documents, metadatas, distances):
                # Convert distance to similarity score (lower distance = higher similarity)
                # For cosine similarity, distance of 0 = perfect match, 2 = opposite
                similarity_score = 1.0 - (distance / 2.0)  # Normalize to 0-1 range
                
                # Filter by similarity threshold if set
                if similarity_score >= self.similarity_threshold:
                    retrieved_docs.append({
                        "id": doc_id,
                        "text": doc_text,
                        "metadata": metadata if metadata else {},
                        "score": similarity_score,
                        "distance": distance
                    })
        
        return retrieved_docs
    
    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the current collection.
        
        Returns:
            Dictionary with collection information
        """
        return self.db_service.get_info()




