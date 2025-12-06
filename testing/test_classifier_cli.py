#!/usr/bin/env python3
"""
Simple CLI tool to test the Query Classifier interactively.

Usage:
    python test_classifier_cli.py
    python test_classifier_cli.py "What is my daily transaction limit?"
"""

import sys
from pathlib import Path

# Add project root to path (go up one level from testing/)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from langgraph.graph.query_classifier import QueryClassifier, QueryType


def print_classification(query: str, query_type: QueryType, confidence: float, metadata: dict):
    """Print classification results in a readable format."""
    print("\n" + "=" * 70)
    print(f"Query: {query}")
    print("-" * 70)
    print(f"Type: {query_type.value.upper()}")
    print(f"Confidence: {confidence:.2%}")
    print(f"Reason: {metadata.get('reason', 'N/A')}")
    
    if 'matched_keywords' in metadata and metadata['matched_keywords']:
        print(f"Matched Keywords: {', '.join(metadata['matched_keywords'])}")
    
    if 'rag_score' in metadata:
        print(f"RAG Score: {metadata['rag_score']:.2f}")
    
    if 'direct_score' in metadata:
        print(f"Direct Answer Score: {metadata['direct_score']:.2f}")
    
    print("=" * 70 + "\n")


def interactive_mode():
    """Interactive mode - keep asking for queries."""
    classifier = QueryClassifier()
    
    print("\n" + "=" * 70)
    print("  🔍 Query Classifier - Interactive Mode")
    print("=" * 70)
    print("\nEnter queries to classify. Type 'quit' or 'exit' to stop.\n")
    
    while True:
        try:
            query = input("Query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!\n")
                break
            
            if not query:
                continue
            
            # Classify
            query_type, confidence, metadata = classifier.classify_query(query)
            
            # Print results
            print_classification(query, query_type, confidence, metadata)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            import traceback
            traceback.print_exc()


def single_query_mode(query: str):
    """Test a single query."""
    classifier = QueryClassifier()
    query_type, confidence, metadata = classifier.classify_query(query)
    print_classification(query, query_type, confidence, metadata)


def example_queries():
    """Run example queries."""
    classifier = QueryClassifier()
    
    examples = [
        "What is my daily transaction limit?",
        "Hello, how are you?",
        "Tell me a joke",
        "How do I block my card?",
        "Thanks for your help",
        "What is the capital of France?",
        "",
        "xyz",
    ]
    
    print("\n" + "=" * 70)
    print("  📋 Running Example Queries")
    print("=" * 70)
    
    for query in examples:
        query_type, confidence, metadata = classifier.classify_query(query)
        print_classification(query, query_type, confidence, metadata)


def main():
    """Main function."""
    if len(sys.argv) > 1:
        # Single query mode
        query = " ".join(sys.argv[1:])
        single_query_mode(query)
    elif len(sys.argv) == 2 and sys.argv[1] in ['--examples', '-e']:
        # Example queries mode
        example_queries()
    else:
        # Interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()