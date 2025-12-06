#!/usr/bin/env python3
"""
Test script for Milestone 1: Basic Components Setup

This script validates:
- Directory structure exists
- Configuration can be imported
- Settings are accessible
- Settings validation works
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_directory_structure():
    """Test that required directories exist."""
    print("📁 Testing Directory Structure...")
    
    langgraph_dir = project_root / "langgraph"
    config_dir = langgraph_dir / "config"
    
    checks = [
        ("langgraph/", langgraph_dir.exists(), langgraph_dir),
        ("langgraph/__init__.py", (langgraph_dir / "__init__.py").exists(), None),
        ("langgraph/config/", config_dir.exists(), config_dir),
        ("langgraph/config/__init__.py", (config_dir / "__init__.py").exists(), None),
        ("langgraph/config/settings.py", (config_dir / "settings.py").exists(), None),
        ("langgraph/README.md", (langgraph_dir / "README.md").exists(), None),
    ]
    
    all_passed = True
    for name, exists, path in checks:
        status = "✅" if exists else "❌"
        print(f"   {status} {name}")
        if not exists:
            all_passed = False
            if path:
                print(f"      → Creating: {path}")
                path.mkdir(parents=True, exist_ok=True)
    
    if all_passed:
        print("   ✅ All directories and files exist!\n")
    else:
        print("   ❌ Some directories/files are missing!\n")
    
    return all_passed


def test_config_import():
    """Test that configuration can be imported."""
    print("📦 Testing Configuration Import...")
    
    try:
        # Test importing from config module
        from langgraph.config import (
            OLLAMA_EMBED_API_URL,
            OLLAMA_CHAT_API_URL,
            EMBEDDING_MODEL,
            CHAT_MODEL,
            OLLAMA_TIMEOUT,
            CHROMADB_PERSIST_DIRECTORY,
            COLLECTION_NAME,
            RETRIEVAL_TOP_K,
            SIMILARITY_THRESHOLD,
            MAX_CONTEXT_LENGTH,
            ENABLE_CONVERSATION_HISTORY,
            MAX_HISTORY_LENGTH,
        )
        
        print("   ✅ All configuration imports successful!")
        print(f"      → Found {12} configuration constants\n")
        return True
        
    except ImportError as e:
        print(f"   ❌ Import failed: {e}\n")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_settings_access():
    """Test that settings are accessible and have values."""
    print("⚙️  Testing Settings Access...")
    
    try:
        from langgraph.config import (
            OLLAMA_EMBED_API_URL,
            OLLAMA_CHAT_API_URL,
            EMBEDDING_MODEL,
            CHAT_MODEL,
            CHROMADB_PERSIST_DIRECTORY,
            COLLECTION_NAME,
        )
        
        settings = {
            "OLLAMA_EMBED_API_URL": OLLAMA_EMBED_API_URL,
            "OLLAMA_CHAT_API_URL": OLLAMA_CHAT_API_URL,
            "EMBEDDING_MODEL": EMBEDDING_MODEL,
            "CHAT_MODEL": CHAT_MODEL,
            "CHROMADB_PERSIST_DIRECTORY": CHROMADB_PERSIST_DIRECTORY,
            "COLLECTION_NAME": COLLECTION_NAME,
        }
        
        all_valid = True
        for name, value in settings.items():
            if value is None or value == "":
                print(f"   ❌ {name} is empty or None")
                all_valid = False
            else:
                print(f"   ✅ {name} = {value}")
        
        if all_valid:
            print("   ✅ All settings have valid values!\n")
        else:
            print("   ❌ Some settings are invalid!\n")
        
        return all_valid
        
    except Exception as e:
        print(f"   ❌ Error accessing settings: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_settings_validation():
    """Test that settings validation works."""
    print("✅ Testing Settings Validation...")
    
    try:
        from langgraph.config.settings import validate_settings, get_settings_summary
        
        # Test validation
        validate_settings()
        print("   ✅ Settings validation passed!")
        
        # Test summary
        summary = get_settings_summary()
        print(f"   ✅ Settings summary generated!")
        print(f"      → Found {len(summary)} configuration groups")
        print(f"      → Groups: {', '.join(summary.keys())}\n")
        
        return True
        
    except ValueError as e:
        print(f"   ❌ Validation failed: {e}\n")
        return False
    except Exception as e:
        print(f"   ❌ Error during validation: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_settings_summary():
    """Test that settings summary is complete."""
    print("📊 Testing Settings Summary...")
    
    try:
        from langgraph.config.settings import get_settings_summary
        
        summary = get_settings_summary()
        
        expected_groups = ["ollama", "chromadb", "rag", "conversation"]
        missing_groups = [g for g in expected_groups if g not in summary]
        
        if missing_groups:
            print(f"   ❌ Missing groups: {', '.join(missing_groups)}\n")
            return False
        
        print("   ✅ All expected configuration groups present!")
        for group_name, group_settings in summary.items():
            print(f"      → {group_name}: {len(group_settings)} settings")
        print()
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error getting summary: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests for Milestone 1."""
    print("=" * 70)
    print("  🧪 Milestone 1: Basic Components Setup - Testing")
    print("=" * 70)
    print()
    
    results = []
    
    # Test 1: Directory structure
    results.append(("Directory Structure", test_directory_structure()))
    
    # Test 2: Configuration import
    results.append(("Configuration Import", test_config_import()))
    
    # Test 3: Settings access
    results.append(("Settings Access", test_settings_access()))
    
    # Test 4: Settings validation
    results.append(("Settings Validation", test_settings_validation()))
    
    # Test 5: Settings summary
    results.append(("Settings Summary", test_settings_summary()))
    
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
        print("  🎉 Milestone 1 is complete and working correctly!")
        print("  ✅ Ready to proceed to Milestone 2!")
    else:
        print("  ⚠️  Some tests failed. Please fix the issues before proceeding.")
    
    print("=" * 70)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

