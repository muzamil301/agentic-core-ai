#!/usr/bin/env python3
"""
Start only the API server (skip React frontend).

Use this if you're having persistent npm issues.
You can use the Streamlit UI instead.
"""

import subprocess
import sys
import time
from pathlib import Path


def start_api_server():
    """Start the API server."""
    print("🔧 Starting API Server Only...")
    print("=" * 50)
    
    api_dir = Path(__file__).parent / "api"
    
    try:
        print("🚀 Starting FastAPI server...")
        process = subprocess.Popen([
            sys.executable, "simple_main.py"
        ], cwd=api_dir)
        
        print(f"✅ API Server started (PID: {process.pid})")
        print("")
        print("🔗 API Server: http://localhost:8000")
        print("📖 API Docs: http://localhost:8000/docs")
        print("")
        print("🎨 Alternative UIs available:")
        print("   • Streamlit: python langgraph/run_ui.py")
        print("   • CLI: python langgraph/chat.py")
        print("")
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Wait for the process
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping API server...")
            process.terminate()
            print("👋 API server stopped")
        
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")
        return False
    
    return True


def test_api():
    """Test if the API is working."""
    print("🧪 Testing API endpoints...")
    
    import requests
    import time
    
    # Wait for server to start
    time.sleep(2)
    
    try:
        # Test status endpoint
        response = requests.get("http://localhost:8000/status", timeout=5)
        if response.status_code == 200:
            print("✅ API is responding correctly")
            data = response.json()
            print(f"   Status: {data.get('service_status', 'unknown')}")
            print(f"   RAG Service: {'Available' if data.get('connected') else 'Not Available'}")
        else:
            print(f"⚠️  API responded with status {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"❌ API test failed: {e}")
        print("   The API might still be starting up...")


def main():
    """Main function."""
    print("🎯 RAG Chat API - Server Only Mode")
    print("This starts just the API server, skipping React frontend")
    print("")
    
    # Check if we can import the RAG service
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from langgraph.service.rag_service import RAGService
        print("✅ RAG service imports successfully")
    except Exception as e:
        print(f"⚠️  RAG service import issue: {e}")
        print("   API will run in limited mode")
    
    print("")
    
    # Start the API server
    if start_api_server():
        print("✅ API server session completed")
    else:
        print("❌ Failed to start API server")
        sys.exit(1)


if __name__ == "__main__":
    main()
