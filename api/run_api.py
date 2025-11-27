#!/usr/bin/env python3
"""
Launcher script for the FastAPI backend.

This script starts the FastAPI server that connects React frontend with LangGraph.
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Launch the FastAPI server."""
    # Get the path to the main API file
    api_path = Path(__file__).parent / "main.py"
    
    if not api_path.exists():
        print(f"❌ API file not found at: {api_path}")
        sys.exit(1)
    
    print("🚀 Starting RAG Chat API Server...")
    print("🔗 API will be available at: http://localhost:8000")
    print("📖 API documentation at: http://localhost:8000/docs")
    print("🌐 Frontend should connect to: http://localhost:8000")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Launch FastAPI with uvicorn
        subprocess.run([
            sys.executable, "-m", "uvicorn", "main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload",
            "--log-level", "info"
        ], cwd=Path(__file__).parent)
    except KeyboardInterrupt:
        print("\n👋 Shutting down the API server...")
    except Exception as e:
        print(f"❌ Error launching API server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
