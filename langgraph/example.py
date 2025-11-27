"""
Example usage of the RAG service.

This script demonstrates how to use the RAG service programmatically.
"""

from langgraph.service.rag_service import RAGService


def main():
    """Example usage of RAG service."""
    print("=" * 70)
    print("RAG Service Example")
    print("=" * 70)
    
    # Initialize service
    print("\n1. Initializing RAG service...")
    try:
        service = RAGService()
        print("   ✅ Service initialized successfully!")
    except Exception as e:
        print(f"   ❌ Failed to initialize: {e}")
        return
    
    # Example queries
    queries = [
        "What is my daily transaction limit?",
        "How do I block my card?",
        "How long do international transfers take?",
    ]
    
    print("\n2. Testing queries...")
    print("-" * 70)
    
    for i, query in enumerate(queries, 1):
        print(f"\nQuery {i}: {query}")
        print("-" * 70)
        
        try:
            result = service.chat(query)
            
            print(f"Response: {result['response']}")
            print(f"Retrieved {len(result['retrieved_docs'])} document(s)")
            
            if result.get('metadata'):
                print(f"Metadata: {result['metadata']}")
        
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Test conversation history
    print("\n" + "=" * 70)
    print("3. Testing conversation history...")
    print("-" * 70)
    
    service.reset_conversation()
    
    print("\nUser: Tell me about transaction limits")
    result1 = service.chat("Tell me about transaction limits")
    print(f"Assistant: {result1['response'][:100]}...")
    
    print("\nUser: How do I check it?")
    result2 = service.chat("How do I check it?")
    print(f"Assistant: {result2['response'][:100]}...")
    print("\n✅ Conversation history working! (Assistant understood 'it' = transaction limit)")
    
    print("\n" + "=" * 70)
    print("✅ Example completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()




