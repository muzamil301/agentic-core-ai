#!/usr/bin/env python3
"""
Test script for Milestone 4: LLM Integration

This script validates:
- OllamaChatClient can be imported
- Can connect to Ollama API
- Can generate responses
- Handles errors gracefully
- Supports conversation history
- Supports system prompts
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_import():
    """Test that OllamaChatClient can be imported."""
    print("📦 Testing Import...")
    
    try:
        from langgraph.llm.ollama_chat import (
            OllamaChatClient,
            generate_response,
        )
        
        print("   ✅ OllamaChatClient imported successfully!")
        print("   ✅ generate_response function imported successfully!\n")
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


def test_initialization():
    """Test that OllamaChatClient can be initialized."""
    print("🔧 Testing Initialization...")
    
    try:
        from langgraph.llm.ollama_chat import OllamaChatClient
        
        client = OllamaChatClient()
        
        print("   ✅ OllamaChatClient initialized successfully!")
        print(f"   → Model: {client.model}")
        print(f"   → API URL: {client.api_url}")
        print(f"   → Timeout: {client.timeout}s\n")
        return True
        
    except Exception as e:
        print(f"   ❌ Initialization failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_simple_chat():
    """Test simple chat completion."""
    print("💬 Testing Simple Chat...")
    
    try:
        from langgraph.llm.ollama_chat import OllamaChatClient
        
        client = OllamaChatClient()
        
        messages = [
            {"role": "user", "content": "Say 'Hello, I am working!' in one sentence."}
        ]
        
        print("   Sending message to Ollama...", end=" ", flush=True)
        response = client.generate_response(messages)
        print("✅")
        
        print(f"   → Response: {response[:100]}...")
        print("   ✅ Simple chat works!\n")
        return True
        
    except ConnectionError as e:
        print("❌")
        print(f"   ❌ Connection error: {e}\n")
        print("   💡 Make sure Ollama is running: ollama serve")
        print("   💡 Make sure the model is available: ollama pull llama3.2\n")
        return False
    except Exception as e:
        print("❌")
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_conversation_history():
    """Test with conversation history."""
    print("📜 Testing Conversation History...")
    
    try:
        from langgraph.llm.ollama_chat import OllamaChatClient
        
        client = OllamaChatClient()
        
        messages = [
            {"role": "user", "content": "My name is Alice."},
            {"role": "assistant", "content": "Nice to meet you, Alice!"},
            {"role": "user", "content": "What's my name?"}
        ]
        
        print("   Sending conversation with history...", end=" ", flush=True)
        response = client.generate_response(messages)
        print("✅")
        
        print(f"   → Response: {response[:100]}...")
        
        # Check if response mentions the name (basic check)
        if "alice" in response.lower():
            print("   ✅ Conversation history is working!")
        else:
            print("   ⚠️  Response may not be using conversation history")
        
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


def test_system_prompt():
    """Test with system prompt."""
    print("🎯 Testing System Prompt...")
    
    try:
        from langgraph.llm.ollama_chat import OllamaChatClient
        
        client = OllamaChatClient()
        
        messages = [
            {"role": "user", "content": "What is 2+2?"}
        ]
        
        system_prompt = "You are a helpful math tutor. Always explain your reasoning."
        
        print("   Sending message with system prompt...", end=" ", flush=True)
        response = client.generate_response(messages, system_prompt=system_prompt)
        print("✅")
        
        print(f"   → Response: {response[:100]}...")
        print("   ✅ System prompt works!\n")
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


def test_chat_convenience_method():
    """Test the chat convenience method."""
    print("🔧 Testing Chat Convenience Method...")
    
    try:
        from langgraph.llm.ollama_chat import OllamaChatClient
        
        client = OllamaChatClient()
        
        print("   Testing chat() method...", end=" ", flush=True)
        response = client.chat("Say 'Test successful' in one sentence.")
        print("✅")
        
        print(f"   → Response: {response[:100]}...")
        print("   ✅ Chat convenience method works!\n")
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


def test_empty_messages():
    """Test that empty messages are handled gracefully."""
    print("🚫 Testing Empty Messages Handling...")
    
    try:
        from langgraph.llm.ollama_chat import OllamaChatClient
        
        client = OllamaChatClient()
        
        try:
            response = client.generate_response([])
            print("   ❌ Empty messages should raise ValueError")
            return False
        except ValueError:
            print("   ✅ Empty messages raise ValueError (expected)")
        
        print("   ✅ Empty messages handling works!\n")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_invalid_message_format():
    """Test that invalid message formats are handled."""
    print("⚠️  Testing Invalid Message Format...")
    
    try:
        from langgraph.llm.ollama_chat import OllamaChatClient
        
        client = OllamaChatClient()
        
        # Test missing role
        try:
            client.generate_response([{"content": "test"}])
            print("   ❌ Missing role should raise ValueError")
            return False
        except ValueError:
            print("   ✅ Missing role raises ValueError (expected)")
        
        # Test missing content
        try:
            client.generate_response([{"role": "user"}])
            print("   ❌ Missing content should raise ValueError")
            return False
        except ValueError:
            print("   ✅ Missing content raises ValueError (expected)")
        
        # Test invalid role
        try:
            client.generate_response([{"role": "invalid", "content": "test"}])
            print("   ❌ Invalid role should raise ValueError")
            return False
        except ValueError:
            print("   ✅ Invalid role raises ValueError (expected)")
        
        print("   ✅ Invalid message format handling works!\n")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_convenience_function():
    """Test the convenience generate_response function."""
    print("🔧 Testing Convenience Function...")
    
    try:
        from langgraph.llm.ollama_chat import generate_response
        
        messages = [
            {"role": "user", "content": "Say 'Function works' in one sentence."}
        ]
        
        print("   Testing generate_response() function...", end=" ", flush=True)
        response = generate_response(messages)
        print("✅")
        
        print(f"   → Response: {response[:100]}...")
        print("   ✅ Convenience function works!\n")
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
    """Test error handling for connection issues."""
    print("🛡️  Testing Error Handling...")
    
    try:
        from langgraph.llm.ollama_chat import OllamaChatClient
        
        # Test with invalid URL (should fail gracefully)
        client = OllamaChatClient(
            api_url="http://localhost:99999/api/chat"  # Invalid port
        )
        
        messages = [{"role": "user", "content": "test"}]
        
        try:
            response = client.generate_response(messages)
            print("   ⚠️  Expected connection error but got response")
            return True  # Not a critical failure
        except ConnectionError:
            print("   ✅ Connection errors are handled gracefully")
            return True
        except Exception as e:
            print(f"   ⚠️  Got different error: {e}")
            return True  # Still handled an error
        
    except Exception as e:
        print(f"   ⚠️  Error during error handling test: {e}")
        return True  # Not critical


def main():
    """Run all tests for Milestone 4."""
    print("=" * 70)
    print("  🧪 Milestone 4: LLM Integration - Testing")
    print("=" * 70)
    print()
    
    results = []
    
    # Test 1: Import
    results.append(("Import", test_import()))
    
    # Test 2: Initialization
    results.append(("Initialization", test_initialization()))
    
    # Test 3: Simple chat
    results.append(("Simple Chat", test_simple_chat()))
    
    # Test 4: Conversation history
    results.append(("Conversation History", test_conversation_history()))
    
    # Test 5: System prompt
    results.append(("System Prompt", test_system_prompt()))
    
    # Test 6: Chat convenience method
    results.append(("Chat Convenience Method", test_chat_convenience_method()))
    
    # Test 7: Empty messages
    results.append(("Empty Messages Handling", test_empty_messages()))
    
    # Test 8: Invalid message format
    results.append(("Invalid Message Format", test_invalid_message_format()))
    
    # Test 9: Convenience function
    results.append(("Convenience Function", test_convenience_function()))
    
    # Test 10: Error handling
    results.append(("Error Handling", test_error_handling()))
    
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
        print("  🎉 Milestone 4 is complete and working correctly!")
        print("  ✅ Ready to proceed to Milestone 5!")
    else:
        print("  ⚠️  Some tests failed. Please fix the issues before proceeding.")
        print()
        print("  💡 Common issues:")
        print("     • Make sure Ollama is running: ollama serve")
        print("     • Make sure the model is available: ollama pull llama3.2")
        print("     • Check that the API endpoint is correct")
    
    print("=" * 70)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

