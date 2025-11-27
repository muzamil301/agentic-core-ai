"""
Configuration constants for the embeddings project.
"""

# Ollama API Configuration
OLLAMA_API_URL = "http://localhost:11434/api/embed"
EMBEDDING_MODEL = "all-minilm"
OLLAMA_TIMEOUT = 15  # seconds

# ChromaDB Configuration
CHROMADB_PERSIST_DIRECTORY = "./chroma_db"
DEFAULT_COLLECTION_NAME = "customer_support_embeddings"

# Default Collection Metadata
DEFAULT_COLLECTION_METADATA = {"hnsw:space": "cosine"}

