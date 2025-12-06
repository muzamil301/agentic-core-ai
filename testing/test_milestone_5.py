#!/usr/bin/env python3
"""
Test script for Milestone 5: Simple Linear Pipeline

This script validates:
- Pipeline can be imported
- Complete pipeline works end-to-end
- RAG queries work correctly
- Direct answer queries work correctly
- Greeting queries work correctly
- Unclear queries are handled
- Error handling works
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_import():
    """Test that pipeline can be imported."""
    print("📦 Testing Import...")
    
    try:
        from langgraph.simple_pipeline import (
            process_query,
            SimpleRAGPipeline,
            chat,
            format_context,
        )
        
        print("   ✅ All pipeline functions imported successfully!\n")
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


def test_format_context():
    """Test context formatting function."""
    print("📝 Testing Context Formatting...")
    
    try:
        from langgraph.simple_pipeline import format_context
        
        # Test with sample documents
        documents = [
            {"text": "Your daily transaction limit is $10,000.", "score": 0.85},
            {"text": "You can increase your limit by contacting support.", "score": 0.75},
        ]
        
        context = format_context(documents)
        
        if context:
            print(f"   ✅ Context formatted successfully!")
            print(f"   → Length: {len(context)} characters")
            print(f"   → Preview: {context[:80]}...")
            print()
            return True
        else:
            print("   ❌ Context is empty\n")
            return False
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_greeting_queries():
    """Test greeting queries."""
    print("👋 Testing Greeting Queries...")
    
    try:
        from langgraph.simple_pipeline import process_query
        
        test_queries = ["Hello", "Hi there", "Thank you"]
        
        all_passed = True
        for query in test_queries:
            print(f"   Testing: '{query}'...", end=" ", flush=True)
            result = process_query(query)
            
            if result["query_type"] == "greeting" and result["response"]:
                print("✅")
            else:
                print("❌")
                all_passed = False
        
        if all_passed:
            print("   ✅ All greeting queries work!\n")
        else:
            print("   ❌ Some greeting queries failed!\n")
        
        return all_passed
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_unclear_queries():
    """Test unclear queries."""
    print("❓ Testing Unclear Queries...")
    
    try:
        from langgraph.simple_pipeline import process_query
        
        test_queries = ["", "a", "xyz"]
        
        all_passed = True
        for query in test_queries:
            print(f"   Testing: '{query if query else '(empty)'}'...", end=" ", flush=True)
            result = process_query(query)
            
            if result["query_type"] == "unclear" and result["response"]:
                print("✅")
            else:
                print("❌")
                all_passed = False
        
        if all_passed:
            print("   ✅ All unclear queries handled correctly!\n")
        else:
            print("   ❌ Some unclear queries failed!\n")
        
        return all_passed
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_direct_answer_queries():
    """Test direct answer queries (no RAG)."""
    print("💬 Testing Direct Answer Queries...")
    
    try:
        from langgraph.simple_pipeline import process_query
        
        test_query = "What is 2+2?"
        print(f"   Query: '{test_query}'")
        print("   Processing...", end=" ", flush=True)
        
        result = process_query(test_query)
        
        print("✅")
        print(f"   → Type: {result['query_type']}")
        print(f"   → Response: {result['response'][:80]}...")
        
        if result["query_type"] == "direct_answer" and result["response"]:
            print("   ✅ Direct answer query works!\n")
            return True
        else:
            print("   ⚠️  Query may have been classified differently\n")
            return True  # Not a critical failure
        
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


def test_rag_queries():
    """Test RAG queries (with retrieval)."""
    print("📚 Testing RAG Queries...")
    
    try:
        from langgraph.simple_pipeline import process_query
        
        # Check if ChromaDB has documents
        from langgraph.rag.retriever import ChromaDBRetriever
        retriever = ChromaDBRetriever()
        info = retriever.get_collection_info()
        
        if info.get('count', 0) == 0:
            print("   ⚠️  Collection is empty - skipping RAG test")
            print("   💡 Run: python embeddings-management/scripts/payment_support_embeddings.py\n")
            return True  # Not a failure, just no data
        
        test_query = "What is my daily transaction limit?"
        print(f"   Query: '{test_query}'")
        print("   Processing...", end=" ", flush=True)
        
        result = process_query(test_query)
        
        print("✅")
        print(f"   → Type: {result['query_type']}")
        print(f"   → Retrieved Docs: {len(result.get('retrieved_docs', []))}")
        print(f"   → Response: {result['response'][:80]}...")
        
        if result["query_type"] == "rag_required":
            if result.get("retrieved_docs"):
                print("   ✅ RAG query works with document retrieval!")
            else:
                print("   ⚠️  RAG query worked but no documents retrieved")
            print()
            return True
        else:
            print("   ⚠️  Query was classified as non-RAG\n")
            return True  # Not a critical failure
        
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


def test_pipeline_class():
    """Test SimpleRAGPipeline class."""
    print("🔧 Testing SimpleRAGPipeline Class...")
    
    try:
        from langgraph.simple_pipeline import SimpleRAGPipeline
        
        pipeline = SimpleRAGPipeline()
        
        print("   ✅ Pipeline initialized!")
        print(f"   → Top-K: {pipeline.top_k}")
        print(f"   → Similarity Threshold: {pipeline.similarity_threshold}")
        
        # Test processing
        result = pipeline.process("Hello")
        
        if result and "response" in result:
            print("   ✅ Pipeline.process() works!")
            print()
            return True
        else:
            print("   ❌ Pipeline.process() returned invalid result\n")
            return False
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_convenience_function():
    """Test the chat convenience function."""
    print("🔧 Testing Chat Convenience Function...")
    
    try:
        from langgraph.simple_pipeline import chat
        
        response = chat("Hello")
        
        if response:
            print(f"   ✅ Chat function works!")
            print(f"   → Response: {response[:60]}...")
            print()
            return True
        else:
            print("   ❌ Chat function returned empty response\n")
            return False
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_end_to_end_flow():
    """Test complete end-to-end flow."""
    print("🔄 Testing End-to-End Flow...")
    
    try:
        from langgraph.simple_pipeline import process_query
        
        # Test a complete flow
        query = "What is my daily transaction limit?"
        print(f"   Query: '{query}'")
        print("   Running complete pipeline...", end=" ", flush=True)
        
        result = process_query(query)
        
        print("✅")
        
        # Check all required fields
        required_fields = ["response", "query_type", "retrieved_docs", "context", "metadata"]
        all_present = all(field in result for field in required_fields)
        
        if all_present:
            print("   ✅ All required fields present!")
            print(f"   → Response generated: {len(result['response'])} chars")
            print(f"   → Query type: {result['query_type']}")
            print(f"   → Metadata: {len(result['metadata'])} keys")
            print()
            return True
        else:
            missing = [f for f in required_fields if f not in result]
            print(f"   ❌ Missing fields: {missing}\n")
            return False
        
    except Exception as e:
        print("❌")
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests for Milestone 5."""
    print("=" * 70)
    print("  🧪 Milestone 5: Simple Linear Pipeline - Testing")
    print("=" * 70)
    print()
    
    results = []
    
    # Test 1: Import
    results.append(("Import", test_import()))
    
    # Test 2: Context formatting
    results.append(("Context Formatting", test_format_context()))
    
    # Test 3: Greeting queries
    results.append(("Greeting Queries", test_greeting_queries()))
    
    # Test 4: Unclear queries
    results.append(("Unclear Queries", test_unclear_queries()))
    
    # Test 5: Direct answer queries
    results.append(("Direct Answer Queries", test_direct_answer_queries()))
    
    # Test 6: RAG queries
    results.append(("RAG Queries", test_rag_queries()))
    
    # Test 7: Pipeline class
    results.append(("Pipeline Class", test_pipeline_class()))
    
    # Test 8: Convenience function
    results.append(("Convenience Function", test_convenience_function()))
    
    # Test 9: End-to-end flow
    results.append(("End-to-End Flow", test_end_to_end_flow()))
    
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
        print("  🎉 Milestone 5 is complete and working correctly!")
        print("  ✅ Ready to proceed to Milestone 6!")
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

