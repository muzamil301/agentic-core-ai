import requests
import json
import numpy as np # Used for cleaner array printing (optional)
from config import OLLAMA_API_URL, EMBEDDING_MODEL, OLLAMA_TIMEOUT

# 2. Mock Data
mock_data = [
    "The agentic AI project is complex but exciting.",
    "Learning embeddings is a crucial first step for RAG.",
    "A regular expression is a sequence of characters that forms a search pattern.",
]

# 3. Prepare the request payload
# We'll send a batch of inputs to be efficient
payload = {
    "model": EMBEDDING_MODEL,
    "input": mock_data
}

print(f"Sending {len(mock_data)} texts to Ollama API for embedding...")

# 4. Make the API Call
try:
    # Set a timeout just in case the model takes a moment to load
    response = requests.post(OLLAMA_API_URL, json=payload, timeout=OLLAMA_TIMEOUT)
    response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

    # Parse the JSON response
    result = response.json()
    embeddings = result.get("embeddings", [])

    print("✅ Embeddings received successfully.")

    # 5. Review the results (optional print, but good for understanding)
    for i, vector in enumerate(embeddings):
        # Convert the list to a NumPy array for cleaner size display
        vector_array = np.array(vector) 
        
        # Display the text, the vector size, and the first few values
        print("-" * 50)
        print(f"Text {i+1}: '{mock_data[i]}'")
        print(f"Vector Dimension (Size): {vector_array.shape[0]}")
        print(f"First 5 values: {vector_array[:5]}")
        
    print("-" * 50)

except requests.exceptions.RequestException as e:
    print(f"❌ Error connecting to Ollama: {e}")
    print("Please ensure the Ollama service is running in the background.")

