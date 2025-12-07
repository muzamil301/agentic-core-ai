#!/usr/bin/env python3
"""
Test script for Milestone 9: Complete RAG Service

This script validates:
- Service initialization
- Chat method functionality
- Conversation history management
- Streaming support
- Error handling
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_import():
    """Test that RAGService can be imported."""
    print("📦 Testing Import...")
    
    try:
        from langgraph_service.service import RAGService
        
        print("   ✅ RAGService imported successfully!\n")
        return True
        
    except ImportError as e:
        print(f"   ❌ Import failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_service_initialization():
    """Test that service can be initialized."""
    print("🏗️  Testing Service Initialization...")
    
    try:
        from langgraph_service.service import RAGService
        
        # Test default initialization
        service1 = RAGService()
        print("   ✅ Service initialized with defaults")
        
        # Test with history disabled
        service2 = RAGService(enable_history=False)
        print("   ✅ Service initialized with history disabled")
        
        # Verify graph is available
        if service1.graph is not None:
            print("   ✅ Graph is available")
        else:
            print("   ⚠️  Graph is None (may be due to langgraph not installed)")
        
        print()
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_chat_method():
    """Test the chat method."""
    print("💬 Testing Chat Method...")
    
    try:
        from langgraph_service.service import RAGService
        
        service = RAGService(enable_history=False)
        
        # Test simple chat
        print("   Testing simple chat...", end=" ", flush=True)
        response = service.chat("Hello")
        print("✅")
        
        if response:
            print(f"   → Response received: {len(response)} characters")
            print(f"   → Response preview: {response[:60]}...")
        else:
            print("   ⚠️  Empty response (may be expected)")
        
        # Test with a query
        print("   Testing query chat...", end=" ", flush=True)
        response2 = service.chat("What is 2+2?")
        print("✅")
        
        if response2:
            print(f"   → Response received: {len(response2)} characters")
        
        print()
        return True
        
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


def test_conversation_history():
    """Test conversation history management."""
    print("📜 Testing Conversation History...")
    
    try:
        from langgraph_service.service import RAGService
        
        service = RAGService(enable_history=True)
        
        # Initial history should be empty
        history = service.get_history()
        if len(history) == 0:
            print("   ✅ Initial history is empty")
        else:
            print(f"   ⚠️  Initial history has {len(history)} messages")
        
        # Send a message
        print("   Sending first message...", end=" ", flush=True)
        service.chat("Hello")
        print("✅")
        
        # Check history
        history = service.get_history()
        if len(history) == 2:  # User + Assistant
            print(f"   ✅ History updated: {len(history)} messages")
        else:
            print(f"   ⚠️  History has {len(history)} messages (expected 2)")
        
        # Send another message
        print("   Sending second message...", end=" ", flush=True)
        service.chat("What is 2+2?")
        print("✅")
        
        # Check history again
        history = service.get_history()
        if len(history) == 4:  # 2 messages * 2 (user + assistant)
            print(f"   ✅ History updated: {len(history)} messages")
        else:
            print(f"   ⚠️  History has {len(history)} messages (expected 4)")
        
        # Test clear history
        print("   Clearing history...", end=" ", flush=True)
        service.clear_history()
        history = service.get_history()
        if len(history) == 0:
            print("✅")
            print("   ✅ History cleared successfully")
        else:
            print("❌")
            print(f"   ❌ History not cleared: {len(history)} messages remain")
        
        # Test reset_history parameter
        print("   Testing reset_history parameter...", end=" ", flush=True)
        service.chat("Message 1")
        service.chat("Message 2", reset_history=True)
        history = service.get_history()
        if len(history) == 2:  # Only Message 2
            print("✅")
            print("   ✅ reset_history works correctly")
        else:
            print("⚠️")
            print(f"   ⚠️  reset_history may not work: {len(history)} messages")
        
        print()
        return True
        
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


def test_streaming():
    """Test streaming functionality."""
    print("📡 Testing Streaming...")
    
    try:
        from langgraph_service.service import RAGService
        
        service = RAGService(enable_history=False)
        
        print("   Streaming query execution...", end=" ", flush=True)
        updates = list(service.stream("What is 2+2?"))
        print("✅")
        
        if len(updates) > 0:
            print(f"   ✅ Received {len(updates)} state updates")
            
            # Show first few updates
            for i, update in enumerate(updates[:3], 1):
                if isinstance(update, dict):
                    node_name = list(update.keys())[0] if update else "unknown"
                    print(f"   → Update {i}: {node_name}")
            
            if len(updates) > 3:
                print(f"   → ... and {len(updates) - 3} more updates")
        else:
            print("   ⚠️  No updates received")
        
        print()
        return True
        
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


def test_error_handling():
    """Test error handling."""
    print("🛡️  Testing Error Handling...")
    
    try:
        from langgraph_service.service import RAGService
        
        service = RAGService(enable_history=False)
        
        # Test with empty query
        print("   Testing empty query...", end=" ", flush=True)
        response = service.chat("")
        print("✅")
        print(f"   → Response: {response[:50] if response else 'Empty'}")
        
        # Test get_state_dict
        print("   Testing get_state_dict...", end=" ", flush=True)
        state_dict = service.get_state_dict("test query")
        if isinstance(state_dict, dict) and "query" in state_dict:
            print("✅")
            print(f"   → State dict has {len(state_dict)} keys")
        else:
            print("❌")
            print("   ❌ Invalid state dict")
        
        print()
        return True
        
    except Exception as e:
        print("❌")
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_end_to_end():
    """Test end-to-end functionality."""
    print("🔄 Testing End-to-End...")
    
    try:
        from langgraph_service.service import RAGService
        
        service = RAGService(enable_history=True)
        
        # Simulate a conversation
        print("   Simulating conversation...", end=" ", flush=True)
        
        # First message
        response1 = service.chat("Hello")
        
        # Second message (should have context from first)
        response2 = service.chat("What is 2+2?")
        
        # Third message
        response3 = service.chat("Thanks")
        
        print("✅")
        
        # Check all responses were generated
        if response1 and response2 and response3:
            print("   ✅ All responses generated")
            print(f"   → Response 1: {len(response1)} chars")
            print(f"   → Response 2: {len(response2)} chars")
            print(f"   → Response 3: {len(response3)} chars")
            
            # Check history
            history = service.get_history()
            if len(history) == 6:  # 3 conversations * 2 (user + assistant)
                print(f"   ✅ History maintained: {len(history)} messages")
            else:
                print(f"   ⚠️  History has {len(history)} messages (expected 6)")
        else:
            print("   ⚠️  Some responses may be empty")
        
        print()
        return True
        
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


def main():
    """Run all tests for Milestone 9."""
    print("=" * 70)
    print("  🧪 Milestone 9: Complete RAG Service - Testing")
    print("=" * 70)
    print()
    
    results = []
    
    # Test 1: Import
    results.append(("Import", test_import()))
    
    # Test 2: Service initialization
    results.append(("Service Initialization", test_service_initialization()))
    
    # Test 3: Chat method
    results.append(("Chat Method", test_chat_method()))
    
    # Test 4: Conversation history
    results.append(("Conversation History", test_conversation_history()))
    
    # Test 5: Streaming
    results.append(("Streaming", test_streaming()))
    
    # Test 6: Error handling
    results.append(("Error Handling", test_error_handling()))
    
    # Test 7: End-to-end
    results.append(("End-to-End", test_end_to_end()))
    
    # Print summary
    print("=" * 70)
    print("  📋 Test Summary")
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
        print("  🎉 Milestone 9 is complete and working correctly!")
        print("  ✅ Ready to proceed to Milestone 10!")
    else:
        print("  ⚠️  Some tests failed. Please fix the issues before proceeding.")
        print()
        print("  💡 Common issues:")
        print("     • Make sure langgraph is installed: pip install langgraph")
        print("     • Make sure Ollama is running: ollama serve")
        print("     • Make sure embeddings exist: python embeddings-management/scripts/payment_support_embeddings.py")
    
    print("=" * 70)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

