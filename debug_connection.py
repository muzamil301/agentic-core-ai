#!/usr/bin/env python3
"""
Debug script to test API connectivity and diagnose issues.
"""

import requests
import json
import sys
from pathlib import Path


def test_api_endpoints():
    """Test all API endpoints to diagnose issues."""
    base_url = "http://localhost:8000"
    
    print("🔍 Testing API Connectivity")
    print("=" * 50)
    
    # Test 1: Basic connection
    print("\n1️⃣ Testing basic connection...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"   ✅ Root endpoint: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Root endpoint failed: {e}")
        return False
    
    # Test 2: Health check
    print("\n2️⃣ Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   ✅ Health endpoint: {response.status_code}")
        data = response.json()
        print(f"   Status: {data.get('status')}")
        print(f"   RAG Service: {data.get('rag_service_available')}")
    except Exception as e:
        print(f"   ❌ Health endpoint failed: {e}")
    
    # Test 3: Status endpoint
    print("\n3️⃣ Testing status endpoint...")
    try:
        response = requests.get(f"{base_url}/status", timeout=5)
        print(f"   ✅ Status endpoint: {response.status_code}")
        data = response.json()
        print(f"   Connected: {data.get('connected')}")
        print(f"   Service Status: {data.get('service_status')}")
        print(f"   Message: {data.get('message')}")
    except Exception as e:
        print(f"   ❌ Status endpoint failed: {e}")
    
    # Test 4: Chat endpoint
    print("\n4️⃣ Testing chat endpoint...")
    try:
        test_message = {
            "message": "Hello, this is a test",
            "reset_history": False
        }
        
        response = requests.post(
            f"{base_url}/chat", 
            json=test_message,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"   ✅ Chat endpoint: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {data.get('response', 'No response')[:100]}...")
            print(f"   Metadata: {data.get('metadata', {})}")
        else:
            print(f"   ❌ Chat failed with status {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Chat endpoint failed: {e}")
    
    return True


def check_prerequisites():
    """Check if all prerequisites are met."""
    print("\n🔧 Checking Prerequisites")
    print("=" * 50)
    
    # Check if we can import RAG service
    print("\n1️⃣ Checking RAG service import...")
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from langgraph.service.rag_service import RAGService
        print("   ✅ RAG service can be imported")
        
        # Try to initialize
        print("   🔄 Trying to initialize RAG service...")
        service = RAGService()
        print("   ✅ RAG service initialized successfully")
        
        # Test a simple chat
        print("   🔄 Testing RAG service chat...")
        result = service.chat("Hello")
        print(f"   ✅ RAG service working: {result.get('response', '')[:50]}...")
        
    except Exception as e:
        print(f"   ❌ RAG service issue: {e}")
        print("   This might be why the API isn't working properly")
        return False
    
    return True


def test_cors():
    """Test CORS configuration."""
    print("\n🌐 Testing CORS Configuration")
    print("=" * 50)
    
    try:
        # Test with different origins
        origins_to_test = [
            None,  # No origin header
            "http://localhost:3000",
            "http://127.0.0.1:3000", 
            "null"  # File protocol
        ]
        
        for origin in origins_to_test:
            headers = {"Content-Type": "application/json"}
            if origin:
                headers["Origin"] = origin
            
            response = requests.options(
                "http://localhost:8000/chat",
                headers=headers,
                timeout=5
            )
            
            print(f"   Origin '{origin}': {response.status_code}")
            if 'Access-Control-Allow-Origin' in response.headers:
                print(f"      Allowed Origin: {response.headers['Access-Control-Allow-Origin']}")
    
    except Exception as e:
        print(f"   ❌ CORS test failed: {e}")


def main():
    """Main diagnostic function."""
    print("🚀 API Connection Diagnostics")
    print("This will help identify why messages aren't sending")
    print("")
    
    # Step 1: Check prerequisites
    prereq_ok = check_prerequisites()
    
    # Step 2: Test API endpoints
    api_ok = test_api_endpoints()
    
    # Step 3: Test CORS
    test_cors()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 DIAGNOSTIC SUMMARY")
    print("=" * 50)
    
    if not prereq_ok:
        print("❌ ISSUE: RAG service is not working properly")
        print("💡 SOLUTION: Check Ollama and ChromaDB setup")
        print("   1. Ensure Ollama is running: ollama serve")
        print("   2. Check chat model: ollama list")
        print("   3. Verify embeddings: python embeddings-management/scripts/read_embeddings.py")
    
    elif not api_ok:
        print("❌ ISSUE: API server is not responding")
        print("💡 SOLUTION: Restart the API server")
        print("   1. Stop current API server (Ctrl+C)")
        print("   2. Restart: python api/simple_main.py")
    
    else:
        print("✅ API appears to be working correctly")
        print("💡 If HTML still can't send messages, check:")
        print("   1. Browser console for errors (F12)")
        print("   2. Network tab in browser dev tools")
        print("   3. Try refreshing the HTML page")
        print("   4. Try a different browser")
    
    print("\n🔧 Quick fixes to try:")
    print("   • Restart API: python start_api_only.py")
    print("   • Use Streamlit: python langgraph/run_ui.py")
    print("   • Use CLI: python langgraph/chat.py")


if __name__ == "__main__":
    main()
