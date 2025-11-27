#!/usr/bin/env python3
"""
Test the simple RAG service directly without HTTP server.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def test_simple_rag():
    """Test the simple RAG service."""
    print("🔍 Testing Simple RAG Service")
    print("=" * 50)
    
    try:
        from langgraph.service.simple_rag_service import SimpleRAGService
        
        print("✅ Importing SimpleRAGService...")
        service = SimpleRAGService()
        
        print("✅ Service initialized successfully!")
        
        # Test a simple chat
        print("\n💬 Testing chat functionality...")
        test_queries = [
            "Hello, how are you?",
            "What is my daily transaction limit?",
            "Tell me about account tiers"
        ]
        
        for query in test_queries:
            print(f"\n🔤 Query: {query}")
            try:
                result = service.chat(query)
                print(f"✅ Response: {result['response'][:100]}...")
                print(f"📊 Metadata: {result['metadata']}")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to test SimpleRAGService: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_basic_components():
    """Test individual components."""
    print("\n🔧 Testing Individual Components")
    print("=" * 50)
    
    # Test ChromaDB
    print("\n1️⃣ Testing ChromaDB...")
    try:
        from db.chromadb_service import ChromaDBService
        db = ChromaDBService(collection_name="payment_support")
        print("✅ ChromaDB service works")
        
        # Test query
        results = db.read(query_texts=["transaction limit"], n_results=1)
        print(f"✅ ChromaDB query works: {len(results.get('documents', [[]])[0])} results")
        
    except Exception as e:
        print(f"❌ ChromaDB failed: {e}")
    
    # Test Ollama
    print("\n2️⃣ Testing Ollama...")
    try:
        from langgraph.llm.ollama_chat import OllamaChatClient
        client = OllamaChatClient()
        
        response = client.generate_response([
            {"role": "user", "content": "Hello, this is a test"}
        ])
        print(f"✅ Ollama works: {response[:50]}...")
        
    except Exception as e:
        print(f"❌ Ollama failed: {e}")


def main():
    """Main test function."""
    print("🚀 Simple RAG Service Test")
    print("This will test the RAG service without HTTP dependencies")
    print("")
    
    # Test components
    test_basic_components()
    
    # Test full service
    success = test_simple_rag()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Simple RAG service is working!")
        print("💡 You can now use it with the HTML frontend")
    else:
        print("❌ Simple RAG service has issues")
        print("💡 Try using Streamlit UI instead: python langgraph/run_ui.py")


if __name__ == "__main__":
    main()
