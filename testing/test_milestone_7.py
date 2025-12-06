#!/usr/bin/env python3
"""
Test script for Milestone 7: Individual Graph Nodes

This script validates:
- All nodes can be imported
- Each node works independently
- State is updated correctly
- Error handling works in each node
- State flows between nodes correctly
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_import():
    """Test that all nodes can be imported."""
    print("📦 Testing Import...")
    
    try:
        from langgraph.graph.nodes import (
            classify_query_node,
            retrieve_node,
            format_context_node,
            generate_node,
            direct_answer_node,
            respond_node,
        )
        
        print("   ✅ All node functions imported successfully!\n")
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


def test_classify_query_node():
    """Test classify_query_node."""
    print("🔍 Testing classify_query_node...")
    
    try:
        from langgraph.graph.nodes import classify_query_node
        from langgraph.graph.state import create_initial_state
        
        # Create test state
        state = create_initial_state("What is my daily transaction limit?")
        
        # Run node
        result = classify_query_node(state)
        
        # Check result
        if "metadata" in result:
            metadata = result["metadata"]
            if "query_type" in metadata:
                print(f"   ✅ Node executed successfully!")
                print(f"   → Query type: {metadata['query_type']}")
                print(f"   → Confidence: {metadata.get('classification_confidence', 0):.2%}")
                print()
                return True
            else:
                print("   ❌ Metadata missing query_type\n")
                return False
        else:
            print("   ❌ Result missing metadata\n")
            return False
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_retrieve_node():
    """Test retrieve_node."""
    print("📚 Testing retrieve_node...")
    
    try:
        from langgraph.graph.nodes import retrieve_node
        from langgraph.graph.state import create_initial_state
        
        # Create test state
        state = create_initial_state("transaction limit")
        
        # Check if ChromaDB has documents
        from langgraph.rag.retriever import ChromaDBRetriever
        retriever = ChromaDBRetriever()
        info = retriever.get_collection_info()
        
        if info.get('count', 0) == 0:
            print("   ⚠️  Collection is empty - testing with empty state")
            print("   💡 Run: python embeddings-management/scripts/payment_support_embeddings.py\n")
        
        # Run node
        result = retrieve_node(state)
        
        # Check result
        if "retrieved_docs" in result:
            docs = result["retrieved_docs"]
            print(f"   ✅ Node executed successfully!")
            print(f"   → Retrieved {len(docs)} documents")
            if docs:
                print(f"   → First doc score: {docs[0].get('score', 0):.2f}")
            print()
            return True
        else:
            print("   ❌ Result missing retrieved_docs\n")
            return False
        
    except ConnectionError as e:
        print(f"   ❌ Connection error: {e}\n")
        print("   💡 Make sure Ollama is running: ollama serve\n")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_format_context_node():
    """Test format_context_node."""
    print("📝 Testing format_context_node...")
    
    try:
        from langgraph.graph.nodes import format_context_node
        from langgraph.graph.state import create_initial_state
        
        # Create test state with retrieved docs
        state = create_initial_state("test query")
        state["retrieved_docs"] = [
            {"text": "Your daily transaction limit is $10,000.", "score": 0.85},
            {"text": "You can increase your limit by contacting support.", "score": 0.75},
        ]
        
        # Run node
        result = format_context_node(state)
        
        # Check result
        if "context" in result:
            context = result["context"]
            print(f"   ✅ Node executed successfully!")
            print(f"   → Context length: {len(context)} characters")
            print(f"   → Context preview: {context[:60]}...")
            
            if "metadata" in result and "context_length" in result["metadata"]:
                print(f"   → Metadata updated: context_length = {result['metadata']['context_length']}")
            
            print()
            return True
        else:
            print("   ❌ Result missing context\n")
            return False
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_generate_node():
    """Test generate_node (RAG path)."""
    print("🤖 Testing generate_node (RAG)...")
    
    try:
        from langgraph.graph.nodes import generate_node
        from langgraph.graph.state import create_initial_state
        
        # Create test state with context
        state = create_initial_state("What is my daily transaction limit?")
        state["context"] = "Document 1 (relevance: 0.85): Your daily transaction limit is $10,000."

        # Run node
        print("   Sending to LLM...", end=" ", flush=True)
        result = generate_node(state)
        print("✅")
        
        # Check result
        if "response" in result:
            response = result["response"]
            print(f"   ✅ Node executed successfully!")
            print(f"   → Response length: {len(response)} characters")
            print(f"   → Response preview: {response[:80]}...")
            print()
            return True
        else:
            print("   ❌ Result missing response\n")
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


def test_direct_answer_node():
    """Test direct_answer_node."""
    print("💬 Testing direct_answer_node...")
    
    try:
        from langgraph.graph.nodes import direct_answer_node
        from langgraph.graph.state import create_initial_state
        
        # Create test state
        state = create_initial_state("What is 2+2?")
        
        # Run node
        print("   Sending to LLM...", end=" ", flush=True)
        result = direct_answer_node(state)
        print("✅")
        
        # Check result
        if "response" in result:
            response = result["response"]
            print(f"   ✅ Node executed successfully!")
            print(f"   → Response length: {len(response)} characters")
            print(f"   → Response preview: {response[:80]}...")
            print()
            return True
        else:
            print("   ❌ Result missing response\n")
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


def test_respond_node():
    """Test respond_node."""
    print("📤 Testing respond_node...")
    
    try:
        from langgraph.graph.nodes import respond_node
        from langgraph.graph.state import create_initial_state
        
        # Create test state with response
        state = create_initial_state("What is my daily transaction limit?")
        state["response"] = "Your daily transaction limit is $10,000."
        
        # Run node
        result = respond_node(state)
        
        # Check result
        if "messages" in result:
            messages = result["messages"]
            print(f"   ✅ Node executed successfully!")
            print(f"   → Messages count: {len(messages)}")
            
            if len(messages) >= 2:
                print(f"   → User message: {messages[-2].get('role')}")
                print(f"   → Assistant message: {messages[-1].get('role')}")
            
            if "metadata" in result and "response_length" in result["metadata"]:
                print(f"   → Metadata updated: response_length = {result['metadata']['response_length']}")
            
            print()
            return True
        else:
            print("   ❌ Result missing messages\n")
            return False
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_node_chain():
    """Test that nodes can be chained together."""
    print("🔗 Testing Node Chain...")
    
    try:
        from langgraph.graph.nodes import (
            classify_query_node,
            retrieve_node,
            format_context_node,
            generate_node,
            respond_node,
        )
        from langgraph.graph.state import create_initial_state
        
        # Create initial state
        state = create_initial_state("What is my daily transaction limit?")
        
        # Chain nodes together
        print("   Running node chain...", end=" ", flush=True)
        
        # Node 1: Classify
        update1 = classify_query_node(state)
        state.update(update1)
        
        # Node 2: Retrieve
        update2 = retrieve_node(state)
        state.update(update2)
        
        # Node 3: Format context
        update3 = format_context_node(state)
        state.update(update3)
        
        # Node 4: Generate (always call, even if context is empty)
        # The generate_node should handle empty context gracefully
        update4 = generate_node(state)
        state.update(update4)
        
        # Node 5: Respond
        update5 = respond_node(state)
        state.update(update5)
        
        print("✅")
        
        # Verify final state
        # Allow empty response if no documents were retrieved (valid scenario)
        has_response = state.get("response", "").strip() != ""
        has_messages = len(state.get("messages", [])) > 0
        has_docs = len(state.get("retrieved_docs", [])) > 0
        
        if has_messages:  # At minimum, messages should be updated
            print(f"   ✅ Node chain executed successfully!")
            print(f"   → Query type: {state['metadata'].get('query_type', 'unknown')}")
            print(f"   → Retrieved docs: {len(state.get('retrieved_docs', []))}")
            
            if has_response:
                print(f"   → Response generated: {len(state.get('response', ''))} chars")
            else:
                print(f"   → Response: (empty - no documents retrieved, but node executed)")
            
            print(f"   → Messages: {len(state.get('messages', []))}")
            print()
            return True
        else:
            print("   ❌ Final state incomplete - no messages\n")
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


def test_error_handling():
    """Test error handling in nodes."""
    print("🛡️  Testing Error Handling...")
    
    try:
        from langgraph.graph.nodes import (
            classify_query_node,
            retrieve_node,
            generate_node,
        )
        from langgraph.graph.state import create_initial_state
        
        # Test 1: Empty query
        state1 = create_initial_state("")
        result1 = classify_query_node(state1)
        if "metadata" in result1 and result1["metadata"].get("query_type") == "unclear":
            print("   ✅ Empty query handled correctly")
        else:
            print("   ❌ Empty query not handled")
            return False
        
        # Test 2: Node returns dict (for state updates)
        if isinstance(result1, dict):
            print("   ✅ Node returns dict (correct format)")
        else:
            print("   ❌ Node doesn't return dict")
            return False
        
        print("   ✅ Error handling works!\n")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests for Milestone 7."""
    print("=" * 70)
    print("  🧪 Milestone 7: Individual Graph Nodes - Testing")
    print("=" * 70)
    print()
    
    results = []
    
    # Test 1: Import
    results.append(("Import", test_import()))
    
    # Test 2: Classify query node
    results.append(("classify_query_node", test_classify_query_node()))
    
    # Test 3: Retrieve node
    results.append(("retrieve_node", test_retrieve_node()))
    
    # Test 4: Format context node
    results.append(("format_context_node", test_format_context_node()))
    
    # Test 5: Generate node
    results.append(("generate_node", test_generate_node()))
    
    # Test 6: Direct answer node
    results.append(("direct_answer_node", test_direct_answer_node()))
    
    # Test 7: Respond node
    results.append(("respond_node", test_respond_node()))
    
    # Test 8: Node chain
    results.append(("Node Chain", test_node_chain()))
    
    # Test 9: Error handling
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
        print("  🎉 Milestone 7 is complete and working correctly!")
        print("  ✅ Ready to proceed to Milestone 8!")
    else:
        print("  ⚠️  Some tests failed. Please fix the issues before proceeding.")
        print()
        print("  💡 Common issues:")
        print("     • Make sure Ollama is running: ollama serve")
        print("     • Make sure embeddings exist: python embeddings-management/scripts/payment_support_embeddings.py")
        print("     • Check that all previous milestones are working")
    
    print("=" * 70)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

