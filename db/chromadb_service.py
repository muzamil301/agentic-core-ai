import chromadb
import uuid
from typing import List, Optional, Dict, Any
from config import (
    CHROMADB_PERSIST_DIRECTORY,
    DEFAULT_COLLECTION_NAME,
    DEFAULT_COLLECTION_METADATA
)


class ChromaDBService:
    """
    Manages ChromaDB client connection and provides CRUD operations for embeddings.
    """
    
    def __init__(
        self,
        collection_name: str = DEFAULT_COLLECTION_NAME,
        persist_directory: str = CHROMADB_PERSIST_DIRECTORY,
        create_collection: bool = True
    ):
        """
        Initialize ChromaDB client connection and optionally set up a collection.
        
        Args:
            collection_name: Name of the ChromaDB collection
            persist_directory: Directory to persist ChromaDB data
            create_collection: Whether to automatically create/load the collection
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.client: Optional[chromadb.PersistentClient] = None
        self.collection: Optional[chromadb.Collection] = None
        self._connect()
        
        if create_collection:
            self.collection = self.get_collection(
                collection_name=collection_name,
                create_if_not_exists=True
            )
    
    def _connect(self) -> None:
        """Establish connection to ChromaDB."""
        try:
            self.client = chromadb.PersistentClient(path=self.persist_directory)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to ChromaDB: {e}")
    
    def get_collection(
        self, 
        collection_name: str, 
        create_if_not_exists: bool = True,
        metadata: Optional[dict] = None
    ) -> chromadb.Collection:
        """
        Get or create a ChromaDB collection.
        
        Args:
            collection_name: Name of the collection
            create_if_not_exists: Whether to create collection if it doesn't exist
            metadata: Optional metadata for the collection
        
        Returns:
            ChromaDB Collection object
        """
        if self.client is None:
            self._connect()
        
        default_metadata = DEFAULT_COLLECTION_METADATA.copy()
        if metadata:
            default_metadata.update(metadata)
        
        if create_if_not_exists:
            return self.client.get_or_create_collection(
                name=collection_name,
                metadata=default_metadata
            )
        else:
            return self.client.get_collection(name=collection_name)
    
    def set_collection(self, collection_name: str, create_if_not_exists: bool = True) -> None:
        """
        Set the active collection for CRUD operations.
        
        Args:
            collection_name: Name of the collection
            create_if_not_exists: Whether to create collection if it doesn't exist
        """
        self.collection_name = collection_name
        self.collection = self.get_collection(
            collection_name=collection_name,
            create_if_not_exists=create_if_not_exists
        )
    
    def list_collections(self) -> list:
        """
        List all collections in the database.
        
        Returns:
            List of collection names
        """
        if self.client is None:
            self._connect()
        
        collections = self.client.list_collections()
        return [col.name for col in collections]
    
    def delete_collection(self, collection_name: str) -> None:
        """
        Delete a collection from ChromaDB.
        
        Args:
            collection_name: Name of the collection to delete
        """
        if self.client is None:
            self._connect()
        
        self.client.delete_collection(name=collection_name)
        
        # If deleted collection was the active one, reset it
        if self.collection_name == collection_name:
            self.collection = None
    
    def create(
        self,
        texts: List[str],
        embeddings: List[List[float]],
        ids: Optional[List[str]] = None,
        metadatas: Optional[List[Dict[str, Any]]] = None
    ) -> List[str]:
        """
        Create (write) embeddings to ChromaDB.
        
        Args:
            texts: List of text strings that were embedded
            embeddings: List of embedding vectors (list of floats)
            ids: Optional list of unique IDs for each text. If None, auto-generated.
            metadatas: Optional list of metadata dictionaries for each text
        
        Returns:
            List of IDs that were created
        """
        if self.collection is None:
            raise ValueError("No collection set. Use set_collection() or initialize with create_collection=True")
        
        if len(texts) != len(embeddings):
            raise ValueError("Number of texts must match number of embeddings")
        
        # Generate IDs if not provided
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in texts]
        
        # Prepare metadatas (ChromaDB requires a list of dicts)
        if metadatas is None:
            metadatas = [{} for _ in texts]
        
        # Add embeddings to collection
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            ids=ids,
            metadatas=metadatas
        )
        
        return ids
    
    def read(
        self,
        query_embeddings: Optional[List[List[float]]] = None,
        query_texts: Optional[List[str]] = None,
        n_results: int = 10,
        where: Optional[Dict[str, Any]] = None,
        ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Read/query embeddings from ChromaDB.
        
        Args:
            query_embeddings: List of embedding vectors to search for (similarity search)
            query_texts: List of text strings to search for (will be converted to embeddings)
            n_results: Number of results to return
            where: Optional metadata filter dictionary
            ids: Optional list of specific IDs to retrieve
        
        Returns:
            Dictionary containing:
                - ids: List of result IDs
                - documents: List of text documents
                - embeddings: List of embedding vectors
                - distances: List of similarity distances (if query)
                - metadatas: List of metadata dictionaries
        """
        if self.collection is None:
            raise ValueError("No collection set. Use set_collection() or initialize with create_collection=True")
        
        if ids is not None:
            # Direct retrieval by IDs
            results = self.collection.get(
                ids=ids,
                include=["documents", "embeddings", "metadatas"]
            )
            return results
        
        elif query_embeddings is not None:
            # Similarity search using embeddings
            results = self.collection.query(
                query_embeddings=query_embeddings,
                n_results=n_results,
                where=where,
                include=["documents", "embeddings", "distances", "metadatas"]
            )
            return results
        
        elif query_texts is not None:
            # Similarity search using text (ChromaDB will embed them)
            results = self.collection.query(
                query_texts=query_texts,
                n_results=n_results,
                where=where,
                include=["documents", "embeddings", "distances", "metadatas"]
            )
            return results
        
        else:
            # Get all embeddings in the collection
            results = self.collection.get(
                include=["documents", "embeddings", "metadatas"]
            )
            return results
    
    def update(
        self,
        ids: List[str],
        texts: Optional[List[str]] = None,
        embeddings: Optional[List[List[float]]] = None,
        metadatas: Optional[List[Dict[str, Any]]] = None
    ) -> None:
        """
        Update existing embeddings in ChromaDB.
        
        Args:
            ids: List of IDs to update
            texts: Optional new texts to update
            embeddings: Optional new embeddings to update
            metadatas: Optional new metadatas to update
        """
        if self.collection is None:
            raise ValueError("No collection set. Use set_collection() or initialize with create_collection=True")
        
        if not ids:
            raise ValueError("At least one ID must be provided")
        
        # ChromaDB update requires all fields, so we need to get existing data first
        existing = self.collection.get(ids=ids, include=["documents", "embeddings", "metadatas"])
        
        if not existing["ids"]:
            raise ValueError(f"No documents found with IDs: {ids}")
        
        # Prepare update data
        update_texts = texts if texts is not None else existing["documents"]
        update_embeddings = embeddings if embeddings is not None else existing["embeddings"]
        update_metadatas = metadatas if metadatas is not None else existing["metadatas"]
        
        # Validate lengths
        if len(ids) != len(update_texts) or len(ids) != len(update_embeddings):
            raise ValueError("All update lists must have the same length as ids")
        
        # Delete old entries
        self.collection.delete(ids=ids)
        
        # Add updated entries
        self.collection.add(
            ids=ids,
            documents=update_texts,
            embeddings=update_embeddings,
            metadatas=update_metadatas
        )
    
    def delete(self, ids: Optional[List[str]] = None) -> None:
        """
        Delete embeddings from ChromaDB.
        
        Args:
            ids: List of IDs to delete. If None, deletes all entries in the collection.
        """
        if self.collection is None:
            raise ValueError("No collection set. Use set_collection() or initialize with create_collection=True")
        
        if ids is None:
            # Delete all entries by getting all IDs first
            all_data = self.collection.get()
            if all_data["ids"]:
                self.collection.delete(ids=all_data["ids"])
        else:
            self.collection.delete(ids=ids)
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get information about the current collection.
        
        Returns:
            Dictionary with collection count and metadata
        """
        if self.collection is None:
            raise ValueError("No collection set. Use set_collection() or initialize with create_collection=True")
        
        count = self.collection.count()
        return {
            "collection_name": self.collection_name,
            "count": count,
            "metadata": self.collection.metadata
        }
    
    def clear_collection(self) -> None:
        """Clear all entries from the current collection."""
        self.delete()
    
    def close(self) -> None:
        """Close the connection (for persistent client, this is a no-op)."""
        # PersistentClient doesn't need explicit closing, but we keep this for API consistency
        pass
