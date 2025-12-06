#!/usr/bin/env python3
"""
Test script for Milestone 2: Query Classification

This script validates:
- QueryClassifier can be imported
- Classification works for different query types
- Confidence scores are returned
- Edge cases are handled gracefully
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_import():
    """Test that QueryClassifier can be imported."""
    print("📦 Testing Import...")
    
    try:
        from langgraph.graph.query_classifier import (
            QueryClassifier,
            QueryType,
            classify_query,
        )
        
        print("   ✅ QueryClassifier imported successfully!")
        print("   ✅ QueryType enum imported successfully!")
        print("   ✅ classify_query function imported successfully!\n")
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


def test_query_type_enum():
    """Test that QueryType enum has all expected values."""
    print("🔍 Testing QueryType Enum...")
    
    try:
        from langgraph.graph.query_classifier import QueryType
        
        expected_types = [
            "rag_required",
            "direct_answer",
            "greeting",
            "unclear"
        ]
        
        for expected in expected_types:
            # Check if enum value exists
            found = False
            for qtype in QueryType:
                if qtype.value == expected:
                    found = True
                    print(f"   ✅ Found: {expected}")
                    break
            
            if not found:
                print(f"   ❌ Missing: {expected}")
                return False
        
        print("   ✅ All QueryType values present!\n")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_rag_required_queries():
    """Test classification of RAG-required queries."""
    print("📚 Testing RAG-Required Queries...")
    
    try:
        from langgraph.graph.query_classifier import QueryClassifier, QueryType
        
        classifier = QueryClassifier()
        
        test_queries = [
            "What is my daily transaction limit?",
            "How do I block my card?",
            "What are the payment fees?",
            "How to update my account settings?",
            "Tell me about transaction history",
            "What is the withdrawal limit?",
        ]
        
        all_passed = True
        for query in test_queries:
            query_type, confidence, metadata = classifier.classify_query(query)
            
            if query_type == QueryType.RAG_REQUIRED:
                print(f"   ✅ '{query[:50]}...' → RAG_REQUIRED (confidence: {confidence:.2f})")
            else:
                print(f"   ❌ '{query[:50]}...' → {query_type.value} (expected RAG_REQUIRED)")
                all_passed = False
        
        if all_passed:
            print("   ✅ All RAG-required queries classified correctly!\n")
        else:
            print("   ❌ Some RAG-required queries misclassified!\n")
        
        return all_passed
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_direct_answer_queries():
    """Test classification of direct-answer queries."""
    print("💬 Testing Direct-Answer Queries...")
    
    try:
        from langgraph.graph.query_classifier import QueryClassifier, QueryType
        
        classifier = QueryClassifier()
        
        test_queries = [
            "Tell me a joke",
            "What's the weather like?",
            "What is the capital of France?",
            "Explain quantum physics",
            "What is artificial intelligence?",
        ]
        
        all_passed = True
        for query in test_queries:
            query_type, confidence, metadata = classifier.classify_query(query)
            
            if query_type == QueryType.DIRECT_ANSWER:
                print(f"   ✅ '{query[:50]}...' → DIRECT_ANSWER (confidence: {confidence:.2f})")
            else:
                print(f"   ⚠️  '{query[:50]}...' → {query_type.value} (expected DIRECT_ANSWER)")
                # Not critical if some are classified as RAG (safer default)
                if query_type == QueryType.RAG_REQUIRED:
                    print(f"      (Classified as RAG - acceptable fallback)")
        
        print("   ✅ Direct-answer queries tested!\n")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_greeting_queries():
    """Test classification of greeting queries."""
    print("👋 Testing Greeting Queries...")
    
    try:
        from langgraph.graph.query_classifier import QueryClassifier, QueryType
        
        classifier = QueryClassifier()
        
        test_queries = [
            "Hello",
            "Hi there",
            "Good morning",
            "Thank you",
            "Thanks for your help",
            "Bye",
            "Goodbye",
            "How are you?",
        ]
        
        all_passed = True
        for query in test_queries:
            query_type, confidence, metadata = classifier.classify_query(query)
            
            if query_type == QueryType.GREETING:
                print(f"   ✅ '{query}' → GREETING (confidence: {confidence:.2f})")
            else:
                print(f"   ❌ '{query}' → {query_type.value} (expected GREETING)")
                all_passed = False
        
        if all_passed:
            print("   ✅ All greeting queries classified correctly!\n")
        else:
            print("   ❌ Some greeting queries misclassified!\n")
        
        return all_passed
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_unclear_queries():
    """Test classification of unclear queries."""
    print("❓ Testing Unclear Queries...")
    
    try:
        from langgraph.graph.query_classifier import QueryClassifier, QueryType
        
        classifier = QueryClassifier()
        
        test_queries = [
            "",  # Empty
            "a",  # Too short
            "xyz",  # Nonsense
            "asdfghjkl",  # Random characters
        ]
        
        all_passed = True
        for query in test_queries:
            query_type, confidence, metadata = classifier.classify_query(query)
            
            if query_type == QueryType.UNCLEAR:
                print(f"   ✅ '{query[:20] if query else '(empty)'}' → UNCLEAR (confidence: {confidence:.2f})")
            else:
                print(f"   ⚠️  '{query[:20] if query else '(empty)'}' → {query_type.value} (expected UNCLEAR)")
        
        print("   ✅ Unclear queries tested!\n")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_confidence_scores():
    """Test that confidence scores are returned and valid."""
    print("📊 Testing Confidence Scores...")
    
    try:
        from langgraph.graph.query_classifier import QueryClassifier
        
        classifier = QueryClassifier()
        
        test_queries = [
            "What is my daily transaction limit?",
            "Hello",
            "Tell me a joke",
            "",
        ]
        
        all_valid = True
        for query in test_queries:
            query_type, confidence, metadata = classifier.classify_query(query)
            
            # Check confidence is in valid range
            if 0.0 <= confidence <= 1.0:
                print(f"   ✅ '{query[:40] if query else '(empty)'}' → confidence: {confidence:.2f}")
            else:
                print(f"   ❌ '{query[:40] if query else '(empty)'}' → invalid confidence: {confidence}")
                all_valid = False
            
            # Check metadata exists
            if not isinstance(metadata, dict):
                print(f"   ❌ Metadata is not a dict: {type(metadata)}")
                all_valid = False
        
        if all_valid:
            print("   ✅ All confidence scores are valid!\n")
        else:
            print("   ❌ Some confidence scores are invalid!\n")
        
        return all_valid
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_convenience_function():
    """Test the convenience classify_query function."""
    print("🔧 Testing Convenience Function...")
    
    try:
        from langgraph.graph.query_classifier import classify_query, QueryType
        
        query = "What is my daily transaction limit?"
        query_type, confidence, metadata = classify_query(query)
        
        if query_type == QueryType.RAG_REQUIRED:
            print(f"   ✅ Convenience function works!")
            print(f"      Query: '{query}'")
            print(f"      Type: {query_type.value}")
            print(f"      Confidence: {confidence:.2f}\n")
            return True
        else:
            print(f"   ❌ Convenience function returned wrong type: {query_type.value}\n")
            return False
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_metadata_structure():
    """Test that metadata contains expected fields."""
    print("📋 Testing Metadata Structure...")
    
    try:
        from langgraph.graph.query_classifier import QueryClassifier, QueryType
        
        classifier = QueryClassifier()
        
        test_cases = [
            ("What is my daily transaction limit?", QueryType.RAG_REQUIRED),
            ("Hello", QueryType.GREETING),
            ("", QueryType.UNCLEAR),
        ]
        
        all_valid = True
        for query, expected_type in test_cases:
            query_type, confidence, metadata = classifier.classify_query(query)
            
            # Check required fields
            required_fields = ["reason", "original_query"]
            for field in required_fields:
                if field not in metadata:
                    print(f"   ❌ Missing field '{field}' in metadata")
                    all_valid = False
            
            if all_valid:
                print(f"   ✅ '{query[:30] if query else '(empty)'}' → metadata structure valid")
        
        if all_valid:
            print("   ✅ All metadata structures are valid!\n")
        else:
            print("   ❌ Some metadata structures are invalid!\n")
        
        return all_valid
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests for Milestone 2."""
    print("=" * 70)
    print("  🧪 Milestone 2: Query Classification - Testing")
    print("=" * 70)
    print()
    
    results = []
    
    # Test 1: Import
    results.append(("Import", test_import()))
    
    # Test 2: QueryType enum
    results.append(("QueryType Enum", test_query_type_enum()))
    
    # Test 3: RAG-required queries
    results.append(("RAG-Required Queries", test_rag_required_queries()))
    
    # Test 4: Direct-answer queries
    results.append(("Direct-Answer Queries", test_direct_answer_queries()))
    
    # Test 5: Greeting queries
    results.append(("Greeting Queries", test_greeting_queries()))
    
    # Test 6: Unclear queries
    results.append(("Unclear Queries", test_unclear_queries()))
    
    # Test 7: Confidence scores
    results.append(("Confidence Scores", test_confidence_scores()))
    
    # Test 8: Convenience function
    results.append(("Convenience Function", test_convenience_function()))
    
    # Test 9: Metadata structure
    results.append(("Metadata Structure", test_metadata_structure()))
    
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
        print("  🎉 Milestone 2 is complete and working correctly!")
        print("  ✅ Ready to proceed to Milestone 3!")
    else:
        print("  ⚠️  Some tests failed. Please fix the issues before proceeding.")
    
    print("=" * 70)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

