import requests
import json
import uuid
from typing import List, Dict, Any, Optional
import numpy as np
from config import OLLAMA_API_URL, EMBEDDING_MODEL, OLLAMA_TIMEOUT


def text_to_embeddings(texts: List[str], model: str = EMBEDDING_MODEL, api_url: str = OLLAMA_API_URL) -> List[List[float]]:
    """
    Convert a list of text strings to embeddings using Ollama API.
    
    Args:
        texts: List of text strings to embed
        model: Embedding model name (default: "all-minilm")
        api_url: Ollama API URL (default: "http://localhost:11434/api/embed")
    
    Returns:
        List of embedding vectors (list of floats)
    
    Raises:
        requests.exceptions.RequestException: If API call fails
    """
    if not texts:
        return []
    
    payload = {
        "model": model,
        "input": texts
    }
    
    try:
        response = requests.post(api_url, json=payload, timeout=OLLAMA_TIMEOUT)
        response.raise_for_status()
        
        result = response.json()
        embeddings = result.get("embeddings", [])
        
        return embeddings
        
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Failed to generate embeddings: {e}. Please ensure Ollama is running.")


def json_to_embeddings(
    json_file_path: str,
    text_field: str = "text",
    id_field: Optional[str] = None,
    metadata_fields: Optional[List[str]] = None,
    combine_fields: Optional[List[str]] = None,
    model: str = EMBEDDING_MODEL,
    api_url: str = OLLAMA_API_URL
) -> tuple[List[str], List[List[float]], List[str], List[Dict[str, Any]]]:
    """
    Load JSON file and convert its data to embeddings.
    
    Args:
        json_file_path: Path to the JSON file
        text_field: Field name containing the text to embed (default: "text")
        id_field: Optional field name for IDs. If None, auto-generated.
        metadata_fields: Optional list of field names to include as metadata
        combine_fields: Optional list of field names to combine into text (e.g., ["question", "answer"])
        model: Embedding model name (default: "all-minilm")
        api_url: Ollama API URL (default: "http://localhost:11434/api/embed")
    
    Returns:
        Tuple of (texts, embeddings, ids, metadatas)
    
    Raises:
        FileNotFoundError: If JSON file doesn't exist
        KeyError: If required fields are missing
    """
    # Load JSON file
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON file not found: {json_file_path}")
    
    # Handle both list and single object
    if isinstance(data, dict):
        data = [data]
    
    texts = []
    ids = []
    metadatas = []
    
    for item in data:
        # Prepare text for embedding
        if combine_fields:
            # Combine multiple fields
            text_parts = []
            for field in combine_fields:
                if field in item:
                    text_parts.append(f"{field.capitalize()}: {item[field]}")
            text = " ".join(text_parts)
        elif text_field in item:
            text = item[text_field]
        else:
            raise KeyError(f"Field '{text_field}' not found in JSON data")
        
        texts.append(text)
        
        # Get or generate ID
        if id_field and id_field in item:
            ids.append(str(item[id_field]))
        else:
            ids.append(None)  # Will be auto-generated later
        
        # Prepare metadata
        metadata = {}
        if metadata_fields:
            for field in metadata_fields:
                if field in item:
                    # Handle list values (e.g., keywords)
                    if isinstance(item[field], list):
                        metadata[field] = ", ".join(item[field])
                    else:
                        metadata[field] = item[field]
        else:
            # Include all fields except text and id fields
            for key, value in item.items():
                if key != text_field and key != id_field:
                    if key not in (combine_fields or []):
                        if isinstance(value, list):
                            metadata[key] = ", ".join(value)
                        else:
                            metadata[key] = value
        
        metadatas.append(metadata)
    
    # Generate embeddings
    embeddings = text_to_embeddings(texts, model=model, api_url=api_url)
    
    # Auto-generate IDs for None values
    for i, id_val in enumerate(ids):
        if id_val is None:
            ids[i] = str(uuid.uuid4())
    
    return texts, embeddings, ids, metadatas


def get_embedding_info(embeddings: List[List[float]]) -> Dict[str, Any]:
    """
    Get information about generated embeddings.
    
    Args:
        embeddings: List of embedding vectors
    
    Returns:
        Dictionary with embedding statistics
    """
    if not embeddings:
        return {"count": 0, "dimension": 0}
    
    vector_array = np.array(embeddings[0])
    dimension = vector_array.shape[0]
    
    return {
        "count": len(embeddings),
        "dimension": dimension,
        "sample_values": embeddings[0][:5] if embeddings else []
    }

