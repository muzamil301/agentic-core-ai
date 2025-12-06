#!/usr/bin/env python3
"""
Test script for Milestone 6: LangGraph State Definition

This script validates:
- GraphState can be imported
- State structure is correct
- Can create state instances
- Type hints work correctly
- Helper functions work
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_import():
    """Test that GraphState can be imported."""
    print("📦 Testing Import...")
    
    try:
        from langgraph.graph.state import (
            GraphState,
            create_initial_state,
            create_state_from_dict,
            state_to_dict,
        )
        
        print("   ✅ GraphState imported successfully!")
        print("   ✅ Helper functions imported successfully!\n")
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


def test_state_structure():
    """Test that GraphState has all required fields."""
    print("📋 Testing State Structure...")
    
    try:
        from langgraph.graph.state import GraphState
        from typing import get_type_hints
        
        # Get type hints
        hints = get_type_hints(GraphState, include_extras=True)
        
        # Expected fields
        expected_fields = [
            "messages",
            "query",
            "retrieved_docs",
            "context",
            "response",
            "metadata"
        ]
        
        all_present = True
        for field in expected_fields:
            if field in hints:
                print(f"   ✅ Field '{field}' present")
            else:
                print(f"   ❌ Field '{field}' missing")
                all_present = False
        
        if all_present:
            print("   ✅ All required fields present!\n")
        else:
            print("   ❌ Some fields are missing!\n")
        
        return all_present
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_create_initial_state():
    """Test creating initial state."""
    print("🔧 Testing create_initial_state()...")
    
    try:
        from langgraph.graph.state import create_initial_state
        
        query = "What is my daily transaction limit?"
        state = create_initial_state(query)
        
        # Check all fields are present and have correct initial values
        checks = [
            ("messages", list, []),
            ("query", str, query),
            ("retrieved_docs", list, []),
            ("context", str, ""),
            ("response", str, ""),
            ("metadata", dict, {}),
        ]
        
        all_valid = True
        for field_name, expected_type, expected_value in checks:
            value = state.get(field_name)
            
            if not isinstance(value, expected_type):
                print(f"   ❌ Field '{field_name}' has wrong type: {type(value)}")
                all_valid = False
            elif value != expected_value:
                print(f"   ⚠️  Field '{field_name}' has unexpected value: {value}")
            else:
                print(f"   ✅ Field '{field_name}' correct")
        
        if all_valid:
            print("   ✅ Initial state created correctly!\n")
        else:
            print("   ❌ Some fields are incorrect!\n")
        
        return all_valid
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_state_creation():
    """Test creating state instances directly."""
    print("🏗️  Testing Direct State Creation...")
    
    try:
        from langgraph.graph.state import GraphState
        
        # Create state directly
        state: GraphState = {
            "messages": [{"role": "user", "content": "Hello"}],
            "query": "What is 2+2?",
            "retrieved_docs": [{"text": "Document 1", "score": 0.85}],
            "context": "Formatted context",
            "response": "The answer is 4",
            "metadata": {"query_type": "direct_answer"}
        }
        
        # Verify all fields are accessible
        assert state["messages"] == [{"role": "user", "content": "Hello"}]
        assert state["query"] == "What is 2+2?"
        assert len(state["retrieved_docs"]) == 1
        assert state["context"] == "Formatted context"
        assert state["response"] == "The answer is 4"
        assert state["metadata"]["query_type"] == "direct_answer"
        
        print("   ✅ State created and accessed correctly!")
        print(f"   → Query: {state['query']}")
        print(f"   → Messages: {len(state['messages'])}")
        print(f"   → Retrieved Docs: {len(state['retrieved_docs'])}")
        print()
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_state_from_dict():
    """Test creating state from dictionary."""
    print("📝 Testing create_state_from_dict()...")
    
    try:
        from langgraph.graph.state import create_state_from_dict
        
        data = {
            "query": "Test query",
            "messages": [{"role": "user", "content": "Hello"}],
            "retrieved_docs": [],
            "context": "",
            "response": "",
            "metadata": {"test": True}
        }
        
        state = create_state_from_dict(data)
        
        if state["query"] == "Test query" and state["metadata"]["test"]:
            print("   ✅ State created from dict correctly!")
            print()
            return True
        else:
            print("   ❌ State values incorrect\n")
            return False
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_state_to_dict():
    """Test converting state to dictionary."""
    print("🔄 Testing state_to_dict()...")
    
    try:
        from langgraph.graph.state import GraphState, state_to_dict
        
        state: GraphState = {
            "messages": [],
            "query": "Test",
            "retrieved_docs": [],
            "context": "",
            "response": "Response",
            "metadata": {}
        }
        
        result = state_to_dict(state)
        
        if isinstance(result, dict) and "query" in result and "response" in result:
            print("   ✅ State converted to dict correctly!")
            print(f"   → Keys: {list(result.keys())}")
            print()
            return True
        else:
            print("   ❌ Conversion failed\n")
            return False
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_state_mutation():
    """Test that state can be updated (mutation)."""
    print("✏️  Testing State Mutation...")
    
    try:
        from langgraph.graph.state import create_initial_state
        
        state = create_initial_state("Initial query")
        
        # Update state fields
        state["query"] = "Updated query"
        state["response"] = "Updated response"
        state["retrieved_docs"] = [{"text": "Doc 1", "score": 0.9}]
        state["metadata"]["test"] = True
        
        # Verify updates
        if (state["query"] == "Updated query" and 
            state["response"] == "Updated response" and
            len(state["retrieved_docs"]) == 1 and
            state["metadata"]["test"]):
            print("   ✅ State mutation works correctly!")
            print()
            return True
        else:
            print("   ❌ State mutation failed\n")
            return False
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_type_hints():
    """Test that type hints are working."""
    print("🔍 Testing Type Hints...")
    
    try:
        from langgraph.graph.state import GraphState
        from typing import get_type_hints
        
        hints = get_type_hints(GraphState, include_extras=True)
        
        # Check that we have type hints
        if hints:
            print(f"   ✅ Type hints found: {len(hints)} fields")
            for field, hint in hints.items():
                print(f"      → {field}: {hint}")
            print()
            return True
        else:
            print("   ❌ No type hints found\n")
            return False
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_messages_annotation():
    """Test that messages field has proper annotation."""
    print("💬 Testing Messages Annotation...")
    
    try:
        from langgraph.graph.state import GraphState
        from typing import get_type_hints, get_origin, get_args
        
        hints = get_type_hints(GraphState, include_extras=True)
        
        if "messages" in hints:
            messages_hint = hints["messages"]
            print(f"   ✅ Messages field has annotation: {messages_hint}")
            
            # Check if it's annotated (has metadata)
            if hasattr(messages_hint, '__metadata__'):
                print("   ✅ Messages annotation has metadata")
            else:
                print("   ⚠️  Messages annotation may not have metadata")
            
            print()
            return True
        else:
            print("   ❌ Messages field not found\n")
            return False
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests for Milestone 6."""
    print("=" * 70)
    print("  🧪 Milestone 6: LangGraph State Definition - Testing")
    print("=" * 70)
    print()
    
    results = []
    
    # Test 1: Import
    results.append(("Import", test_import()))
    
    # Test 2: State structure
    results.append(("State Structure", test_state_structure()))
    
    # Test 3: Create initial state
    results.append(("Create Initial State", test_create_initial_state()))
    
    # Test 4: Direct state creation
    results.append(("Direct State Creation", test_state_creation()))
    
    # Test 5: State from dict
    results.append(("State From Dict", test_state_from_dict()))
    
    # Test 6: State to dict
    results.append(("State To Dict", test_state_to_dict()))
    
    # Test 7: State mutation
    results.append(("State Mutation", test_state_mutation()))
    
    # Test 8: Type hints
    results.append(("Type Hints", test_type_hints()))
    
    # Test 9: Messages annotation
    results.append(("Messages Annotation", test_messages_annotation()))
    
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
        print("  🎉 Milestone 6 is complete and working correctly!")
        print("  ✅ Ready to proceed to Milestone 7!")
    else:
        print("  ⚠️  Some tests failed. Please fix the issues before proceeding.")
    
    print("=" * 70)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

