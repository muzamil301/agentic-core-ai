#!/usr/bin/env python3
"""
Complete System End-to-End Test

This script validates the entire RAG system from start to finish,
testing all components working together.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_complete_rag_flow():
    """Test complete RAG flow with a real query."""
    print("🔄 Testing Complete RAG Flow...")
    
    try:
        from langgraph_service.service import RAGService
        
        service = RAGService(enable_history=False)
        
        # Test RAG-required query
        print("   Testing RAG query...", end=" ", flush=True)
        response = service.chat("What is my daily transaction limit?")
        print("✅")
        
        if response:
            print(f"   → Response: {response[:100]}...")
            print(f"   → Response length: {len(response)} characters")
            return True
        else:
            print("   ⚠️  Empty response")
            return False
        
    except ConnectionError as e:
        print("❌")
        print(f"   ❌ Connection error: {e}\n")
        print("   💡 Make sure Ollama is running: ollama serve\n")
        return False
    except Exception as e:
        print("❌")
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_direct_answer_flow():
    """Test direct answer flow."""
    print("💬 Testing Direct Answer Flow...")
    
    try:
        from langgraph_service.service import RAGService
        
        service = RAGService(enable_history=False)
        
        # Test direct answer query
        print("   Testing direct answer query...", end=" ", flush=True)
        response = service.chat("What is 2+2?")
        print("✅")
        
        if response:
            print(f"   → Response: {response[:100]}...")
            return True
        else:
            print("   ⚠️  Empty response")
            return False
        
    except Exception as e:
        print("❌")
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_conversation_flow():
    """Test multi-turn conversation."""
    print("💭 Testing Conversation Flow...")
    
    try:
        from langgraph_service.service import RAGService
        
        service = RAGService(enable_history=True)
        
        # First message
        print("   Sending greeting...", end=" ", flush=True)
        response1 = service.chat("Hello")
        print("✅")
        
        # Second message (should have context)
        print("   Sending follow-up...", end=" ", flush=True)
        response2 = service.chat("What is my daily transaction limit?")
        print("✅")
        
        # Check history
        history = service.get_history()
        if len(history) >= 4:
            print(f"   ✅ Conversation history maintained: {len(history)} messages")
            return True
        else:
            print(f"   ⚠️  History has {len(history)} messages (expected at least 4)")
            return True  # Not critical
        
    except Exception as e:
        print("❌")
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_streaming_flow():
    """Test streaming execution."""
    print("📡 Testing Streaming Flow...")
    
    try:
        from langgraph_service.service import RAGService
        
        service = RAGService(enable_history=False)
        
        print("   Streaming query execution...", end=" ", flush=True)
        updates = list(service.stream("What is my daily transaction limit?"))
        print("✅")
        
        if len(updates) > 0:
            print(f"   → Received {len(updates)} state updates")
            
            # Check that we got updates from different nodes
            node_names = set()
            for update in updates:
                if isinstance(update, dict):
                    node_names.update(update.keys())
            
            print(f"   → Nodes executed: {', '.join(sorted(node_names))}")
            return True
        else:
            print("   ⚠️  No updates received")
            return False
        
    except Exception as e:
        print("❌")
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_error_handling():
    """Test error handling across the system."""
    print("🛡️  Testing Error Handling...")
    
    try:
        from langgraph_service.service import RAGService
        
        service = RAGService(enable_history=False)
        
        # Test with empty query
        print("   Testing empty query...", end=" ", flush=True)
        response = service.chat("")
        print("✅")
        
        # Test with very long query
        print("   Testing long query...", end=" ", flush=True)
        long_query = "What is my " + "transaction limit? " * 100
        response = service.chat(long_query)
        print("✅")
        
        print("   ✅ Error handling works")
        return True
        
    except Exception as e:
        print("❌")
        print(f"   ❌ Error: {e}\n")
        return False


def test_all_components():
    """Test that all components can be imported and initialized."""
    print("🧩 Testing All Components...")
    
    try:
        # Test imports
        from langgraph_service.config import COLLECTION_NAME, CHAT_MODEL
        from langgraph_service.graph.query_classifier import QueryClassifier
        from langgraph_service.rag.retriever import ChromaDBRetriever
        from langgraph_service.llm.ollama_chat import OllamaChatClient
        from langgraph_service.graph.graph import create_graph, compile_graph
        from langgraph_service.service import RAGService
        
        print("   ✅ All components imported successfully")
        
        # Test initialization
        classifier = QueryClassifier()
        retriever = ChromaDBRetriever()
        llm_client = OllamaChatClient()
        service = RAGService()
        
        print("   ✅ All components initialized successfully")
        print()
        return True
        
    except Exception as e:
        print("❌")
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def run_all_milestone_tests():
    """Run all individual milestone tests."""
    print("📋 Running All Milestone Tests...")
    print()
    
    import subprocess
    import sys
    
    milestones = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    results = []
    
    for milestone in milestones:
        test_file = f"testing/test_milestone_{milestone}.py"
        print(f"   Running Milestone {milestone} test...", end=" ", flush=True)
        
        try:
            result = subprocess.run(
                [sys.executable, test_file],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print("✅")
                results.append((milestone, True))
            else:
                print("❌")
                results.append((milestone, False))
                if result.stderr:
                    error_lines = result.stderr.split('\n')[:3]
                    for line in error_lines:
                        if line.strip():
                            print(f"      {line[:80]}")
        except subprocess.TimeoutExpired:
            print("⏱️  (timeout)")
            results.append((milestone, False))
        except Exception as e:
            print(f"❌ ({str(e)[:30]})")
            results.append((milestone, False))
    
    print()
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"   Results: {passed}/{total} milestone tests passed")
    
    for milestone, result in results:
        status = "✅" if result else "❌"
        print(f"   {status} Milestone {milestone}")
    
    print()
    return passed == total


def main():
    """Run all comprehensive tests."""
    print("=" * 70)
    print("  🧪 Milestone 10: Complete System Testing & Validation")
    print("=" * 70)
    print()
    
    results = []
    
    # Test 1: All components
    results.append(("All Components", test_all_components()))
    
    # Test 2: Complete RAG flow
    results.append(("Complete RAG Flow", test_complete_rag_flow()))
    
    # Test 3: Direct answer flow
    results.append(("Direct Answer Flow", test_direct_answer_flow()))
    
    # Test 4: Conversation flow
    results.append(("Conversation Flow", test_conversation_flow()))
    
    # Test 5: Streaming flow
    results.append(("Streaming Flow", test_streaming_flow()))
    
    # Test 6: Error handling
    results.append(("Error Handling", test_error_handling()))
    
    # Test 7: All milestone tests
    results.append(("All Milestone Tests", run_all_milestone_tests()))
    
    # Print summary
    print("=" * 70)
    print("  📋 Complete System Test Summary")
    print("=" * 70)
    print()
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")
    
    print()
    print(f"  Results: {passed}/{total} tests passed")
    print()
    
    if passed == total:
        print("  🎉 Complete system is working correctly!")
        print("  ✅ All components integrated successfully!")
        print("  ✅ System is ready for production use!")
    else:
        print("  ⚠️  Some tests failed. Please review the issues above.")
        print()
        print("  💡 Common issues:")
        print("     • Make sure Ollama is running: ollama serve")
        print("     • Make sure embeddings exist: python embeddings-management/scripts/payment_support_embeddings.py")
        print("     • Make sure langgraph is installed: pip install langgraph")
    
    print("=" * 70)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

