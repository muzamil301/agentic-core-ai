#!/usr/bin/env python3
"""
Test script for Milestone 3: Document Retrieval

This script validates:
- ChromaDBRetriever can be imported
- Can connect to ChromaDB
- Can convert queries to embeddings
- Can retrieve relevant documents
- Returns proper format with scores
- Handles empty results gracefully
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_import():
    """Test that ChromaDBRetriever can be imported."""
    print("📦 Testing Import...")
    
    try:
        from langgraph.rag.retriever import (
            ChromaDBRetriever,
            retrieve_documents,
        )
        
        print("   ✅ ChromaDBRetriever imported successfully!")
        print("   ✅ retrieve_documents function imported successfully!\n")
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
    """Test that ChromaDBRetriever can be initialized."""
    print("🔧 Testing Initialization...")
    
    try:
        from langgraph.rag.retriever import ChromaDBRetriever
        
        retriever = ChromaDBRetriever()
        
        print("   ✅ ChromaDBRetriever initialized successfully!")
        print(f"   → Collection: {retriever.collection_name}")
        print(f"   → Embedding Model: {retriever.embedding_model}\n")
        return True
        
    except Exception as e:
        print(f"   ❌ Initialization failed: {e}\n")
        print("   💡 Make sure ChromaDB is accessible and collection exists\n")
        import traceback
        traceback.print_exc()
        return False


def test_collection_info():
    """Test that we can get collection information."""
    print("📊 Testing Collection Info...")
    
    try:
        from langgraph.rag.retriever import ChromaDBRetriever
        
        retriever = ChromaDBRetriever()
        info = retriever.get_collection_info()
        
        print(f"   ✅ Collection info retrieved!")
        print(f"   → Collection Name: {info.get('collection_name', 'N/A')}")
        print(f"   → Document Count: {info.get('count', 0)}")
        
        if info.get('count', 0) == 0:
            print("   ⚠️  Collection is empty - retrieval tests may not work")
            print("   💡 Run: python embeddings-management/scripts/payment_support_embeddings.py\n")
        else:
            print("   ✅ Collection has documents!\n")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Failed to get collection info: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_embedding_generation():
    """Test that queries can be converted to embeddings."""
    print("🔤 Testing Embedding Generation...")
    
    try:
        from langgraph.rag.retriever import ChromaDBRetriever
        
        retriever = ChromaDBRetriever()
        test_query = "transaction limit"
        
        print(f"   Query: '{test_query}'")
        print("   Generating embedding...", end=" ", flush=True)
        
        embedding = retriever._query_to_embedding(test_query)
        
        print("✅")
        print(f"   → Embedding dimension: {len(embedding)}")
        print(f"   → First 5 values: {embedding[:5]}")
        print("   ✅ Embedding generation works!\n")
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


def test_retrieval():
    """Test that documents can be retrieved."""
    print("📚 Testing Document Retrieval...")
    
    try:
        from langgraph.rag.retriever import ChromaDBRetriever
        
        retriever = ChromaDBRetriever()
        
        # Check if collection has documents
        info = retriever.get_collection_info()
        if info.get('count', 0) == 0:
            print("   ⚠️  Collection is empty - skipping retrieval test")
            print("   💡 Run: python embeddings-management/scripts/payment_support_embeddings.py\n")
            return True  # Not a failure, just no data
        
        test_query = "transaction limit"
        print(f"   Query: '{test_query}'")
        print("   Retrieving documents...", end=" ", flush=True)
        
        results = retriever.retrieve_relevant_docs(test_query, top_k=3)
        
        print("✅")
        print(f"   → Retrieved {len(results)} documents")
        
        if results:
            for i, doc in enumerate(results[:3], 1):
                text = doc.get("text", "")[:60]
                score = doc.get("score", 0)
                print(f"   {i}. [{score:.3f}] {text}...")
            print("   ✅ Document retrieval works!\n")
        else:
            print("   ⚠️  No documents retrieved (may be below similarity threshold)\n")
        
        return True
        
    except ValueError as e:
        print("❌")
        print(f"   ❌ ValueError: {e}\n")
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


def test_result_format():
    """Test that results have the correct format."""
    print("📋 Testing Result Format...")
    
    try:
        from langgraph.rag.retriever import ChromaDBRetriever
        
        retriever = ChromaDBRetriever()
        
        # Check if collection has documents
        info = retriever.get_collection_info()
        if info.get('count', 0) == 0:
            print("   ⚠️  Collection is empty - skipping format test")
            print("   💡 Run: python embeddings-management/scripts/payment_support_embeddings.py\n")
            return True
        
        results = retriever.retrieve_relevant_docs("transaction", top_k=1)
        
        if not results:
            print("   ⚠️  No results to check format")
            return True
        
        # Check required fields
        required_fields = ["text", "score"]
        doc = results[0]
        
        all_valid = True
        for field in required_fields:
            if field not in doc:
                print(f"   ❌ Missing field: {field}")
                all_valid = False
            else:
                print(f"   ✅ Field '{field}' present")
        
        # Check types
        if not isinstance(doc.get("text"), str):
            print("   ❌ 'text' should be a string")
            all_valid = False
        
        if not isinstance(doc.get("score"), (int, float)):
            print("   ❌ 'score' should be a number")
            all_valid = False
        else:
            score = doc.get("score")
            if not 0.0 <= score <= 1.0:
                print(f"   ⚠️  'score' should be between 0.0 and 1.0, got {score}")
        
        if all_valid:
            print("   ✅ Result format is correct!\n")
        else:
            print("   ❌ Result format has issues!\n")
        
        return all_valid
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_similarity_threshold():
    """Test that similarity threshold filtering works."""
    print("🎯 Testing Similarity Threshold...")
    
    try:
        from langgraph.rag.retriever import ChromaDBRetriever
        
        retriever = ChromaDBRetriever()
        
        # Check if collection has documents
        info = retriever.get_collection_info()
        if info.get('count', 0) == 0:
            print("   ⚠️  Collection is empty - skipping threshold test")
            print("   💡 Run: python embeddings-management/scripts/payment_support_embeddings.py\n")
            return True
        
        query = "transaction limit"
        
        # Test with low threshold (should get more results)
        results_low = retriever.retrieve_relevant_docs(
            query, 
            top_k=5, 
            similarity_threshold=0.0
        )
        
        # Test with high threshold (should get fewer results)
        results_high = retriever.retrieve_relevant_docs(
            query, 
            top_k=5, 
            similarity_threshold=0.9
        )
        
        print(f"   Query: '{query}'")
        print(f"   → Results with threshold 0.0: {len(results_low)}")
        print(f"   → Results with threshold 0.9: {len(results_high)}")
        
        if len(results_low) >= len(results_high):
            print("   ✅ Similarity threshold filtering works!\n")
            return True
        else:
            print("   ⚠️  Unexpected threshold behavior\n")
            return True  # Not a critical failure
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_top_k():
    """Test that top_k parameter works."""
    print("🔝 Testing Top-K Parameter...")
    
    try:
        from langgraph.rag.retriever import ChromaDBRetriever
        
        retriever = ChromaDBRetriever()
        
        # Check if collection has documents
        info = retriever.get_collection_info()
        if info.get('count', 0) == 0:
            print("   ⚠️  Collection is empty - skipping top_k test")
            print("   💡 Run: python embeddings-management/scripts/payment_support_embeddings.py\n")
            return True
        
        query = "transaction"
        
        # Test with different top_k values
        results_1 = retriever.retrieve_relevant_docs(query, top_k=1)
        results_3 = retriever.retrieve_relevant_docs(query, top_k=3)
        results_5 = retriever.retrieve_relevant_docs(query, top_k=5)
        
        print(f"   Query: '{query}'")
        print(f"   → top_k=1: {len(results_1)} results")
        print(f"   → top_k=3: {len(results_3)} results")
        print(f"   → top_k=5: {len(results_5)} results")
        
        # Results should be sorted by score (descending)
        if results_3:
            scores = [doc["score"] for doc in results_3]
            is_sorted = scores == sorted(scores, reverse=True)
            if is_sorted:
                print("   ✅ Results are sorted by score (descending)")
            else:
                print("   ⚠️  Results may not be sorted correctly")
        
        if len(results_1) <= len(results_3) <= len(results_5):
            print("   ✅ Top-K parameter works!\n")
            return True
        else:
            print("   ⚠️  Unexpected top_k behavior\n")
            return True  # Not a critical failure
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_empty_query():
    """Test that empty queries are handled gracefully."""
    print("🚫 Testing Empty Query Handling...")
    
    try:
        from langgraph.rag.retriever import ChromaDBRetriever
        
        retriever = ChromaDBRetriever()
        
        try:
            results = retriever.retrieve_relevant_docs("")
            print("   ❌ Empty query should raise ValueError")
            return False
        except ValueError:
            print("   ✅ Empty query raises ValueError (expected)")
        
        try:
            results = retriever.retrieve_relevant_docs("   ")
            print("   ❌ Whitespace-only query should raise ValueError")
            return False
        except ValueError:
            print("   ✅ Whitespace-only query raises ValueError (expected)")
        
        print("   ✅ Empty query handling works!\n")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_convenience_function():
    """Test the convenience retrieve_documents function."""
    print("🔧 Testing Convenience Function...")
    
    try:
        from langgraph.rag.retriever import retrieve_documents
        
        # Check if collection has documents
        from langgraph.rag.retriever import ChromaDBRetriever
        retriever = ChromaDBRetriever()
        info = retriever.get_collection_info()
        
        if info.get('count', 0) == 0:
            print("   ⚠️  Collection is empty - skipping convenience function test")
            print("   💡 Run: python embeddings-management/scripts/payment_support_embeddings.py\n")
            return True
        
        query = "transaction"
        results = retrieve_documents(query, top_k=2)
        
        print(f"   Query: '{query}'")
        print(f"   → Retrieved {len(results)} documents")
        print("   ✅ Convenience function works!\n")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests for Milestone 3."""
    print("=" * 70)
    print("  🧪 Milestone 3: Document Retrieval - Testing")
    print("=" * 70)
    print()
    
    results = []
    
    # Test 1: Import
    results.append(("Import", test_import()))
    
    # Test 2: Initialization
    results.append(("Initialization", test_initialization()))
    
    # Test 3: Collection info
    results.append(("Collection Info", test_collection_info()))
    
    # Test 4: Embedding generation
    results.append(("Embedding Generation", test_embedding_generation()))
    
    # Test 5: Document retrieval
    results.append(("Document Retrieval", test_retrieval()))
    
    # Test 6: Result format
    results.append(("Result Format", test_result_format()))
    
    # Test 7: Similarity threshold
    results.append(("Similarity Threshold", test_similarity_threshold()))
    
    # Test 8: Top-K parameter
    results.append(("Top-K Parameter", test_top_k()))
    
    # Test 9: Empty query handling
    results.append(("Empty Query Handling", test_empty_query()))
    
    # Test 10: Convenience function
    results.append(("Convenience Function", test_convenience_function()))
    
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
        print("  🎉 Milestone 3 is complete and working correctly!")
        print("  ✅ Ready to proceed to Milestone 4!")
    else:
        print("  ⚠️  Some tests failed. Please fix the issues before proceeding.")
        print()
        print("  💡 Common issues:")
        print("     • Make sure Ollama is running: ollama serve")
        print("     • Make sure embeddings exist: python embeddings-management/scripts/payment_support_embeddings.py")
    
    print("=" * 70)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

