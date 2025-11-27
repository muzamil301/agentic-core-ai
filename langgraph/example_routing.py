"""
Example demonstrating intelligent query routing.

This script shows how the enhanced RAG service routes different types of queries
to either RAG retrieval or direct LLM responses.
"""

from langgraph.service.rag_service import RAGService
from langgraph.graph.query_classifier import QueryClassifier


def test_query_classification():
    """Test the query classification system."""
    print("=" * 70)
    print("🧠 Query Classification Testing")
    print("=" * 70)
    
    classifier = QueryClassifier()
    
    test_queries = [
        # RAG-required queries (payment-specific)
        "What is my daily transaction limit?",
        "How do I block my card?",
        "How long do international transfers take?",
        "What are the fees for premium accounts?",
        
        # Direct answer queries (general)
        "Hello, how are you?",
        "What's the weather like today?",
        "Tell me a joke",
        "What time is it?",
        
        # Greetings
        "Hi there!",
        "Good morning",
        "Thanks for your help",
        "Goodbye",
        
        # Unclear queries
        "Help",
        "What?",
        "I don't know",
    ]
    
    for query in test_queries:
        query_type, confidence, metadata = classifier.classify_query(query)
        
        print(f"\n📝 Query: '{query}'")
        print(f"   🎯 Type: {query_type.value}")
        print(f"   📊 Confidence: {confidence:.2f}")
        print(f"   🔍 Reasoning: {', '.join(metadata['reasoning'])}")


def test_intelligent_routing():
    """Test the complete RAG service with intelligent routing."""
    print("\n" + "=" * 70)
    print("🤖 Intelligent Routing Testing")
    print("=" * 70)
    
    try:
        service = RAGService()
        print("✅ RAG service initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize RAG service: {e}")
        return
    
    test_scenarios = [
        {
            "category": "💳 Payment Questions (RAG Expected)",
            "queries": [
                "What is my daily transaction limit?",
                "How do I freeze my card?",
                "How long do SEPA transfers take?",
            ]
        },
        {
            "category": "💬 General Questions (Direct Expected)", 
            "queries": [
                "Hello! How are you today?",
                "What's 2 + 2?",
                "Tell me something interesting",
            ]
        },
        {
            "category": "🤝 Greetings (Direct Expected)",
            "queries": [
                "Hi there!",
                "Good morning!",
                "Thank you for your help",
            ]
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n{scenario['category']}")
        print("-" * 70)
        
        for query in scenario['queries']:
            print(f"\n👤 User: {query}")
            
            try:
                result = service.chat(query, reset_history=True)
                response = result['response']
                metadata = result.get('metadata', {})
                
                print(f"🤖 Assistant: {response[:100]}{'...' if len(response) > 100 else ''}")
                
                # Show routing information
                query_type = metadata.get('query_type', 'unknown')
                response_type = metadata.get('response_type', 'unknown')
                retrieval_count = metadata.get('retrieval_count', 0)
                
                print(f"   📋 Query Type: {query_type}")
                print(f"   🔄 Response Type: {response_type}")
                
                if retrieval_count > 0:
                    print(f"   📚 Retrieved {retrieval_count} documents")
                else:
                    print(f"   🚀 Direct answer (no retrieval)")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")


def test_conversation_flow():
    """Test multi-turn conversation with mixed query types."""
    print("\n" + "=" * 70)
    print("💬 Conversation Flow Testing")
    print("=" * 70)
    
    try:
        service = RAGService()
    except Exception as e:
        print(f"❌ Failed to initialize RAG service: {e}")
        return
    
    conversation = [
        "Hello! I need help with my account.",
        "What is my daily transaction limit?",
        "How do I increase it?",
        "Thank you for the information!",
        "By the way, what's the weather like?",
        "Okay, back to banking - how do I block my card?",
        "Perfect, thanks for all your help!",
    ]
    
    print("🎭 Simulating a realistic conversation...")
    print("-" * 70)
    
    for i, query in enumerate(conversation, 1):
        print(f"\n{i}. 👤 User: {query}")
        
        try:
            result = service.chat(query)
            response = result['response']
            metadata = result.get('metadata', {})
            
            print(f"   🤖 Assistant: {response[:150]}{'...' if len(response) > 150 else ''}")
            
            # Show routing decision
            query_type = metadata.get('query_type', 'unknown')
            print(f"   📊 Routing: {query_type}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")


def main():
    """Run all routing tests."""
    print("🚀 Testing Intelligent Query Routing System")
    print("This demonstrates how queries are classified and routed")
    
    # Test 1: Query Classification
    test_query_classification()
    
    # Test 2: Intelligent Routing
    test_intelligent_routing()
    
    # Test 3: Conversation Flow
    test_conversation_flow()
    
    print("\n" + "=" * 70)
    print("✅ All routing tests completed!")
    print("💡 Try the web UI: python langgraph/run_ui.py")
    print("=" * 70)


if __name__ == "__main__":
    main()
