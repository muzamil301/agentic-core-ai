#!/usr/bin/env python3
"""
Launcher script for the React frontend.

This script starts the React development server.
"""

import subprocess
import sys
import os
from pathlib import Path


def main():
    """Launch the React development server."""
    frontend_dir = Path(__file__).parent
    
    # Check if package.json exists
    package_json = frontend_dir / "package.json"
    if not package_json.exists():
        print(f"❌ package.json not found at: {package_json}")
        print("Please run 'npm install' first in the frontend directory")
        sys.exit(1)
    
    # Check if node_modules exists
    node_modules = frontend_dir / "node_modules"
    if not node_modules.exists():
        print("📦 Installing dependencies...")
        try:
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            sys.exit(1)
    
    print("🚀 Starting React Development Server...")
    print("🌐 Frontend will be available at: http://localhost:3000")
    print("🔗 Make sure API server is running at: http://localhost:8000")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Set environment variables
        env = os.environ.copy()
        env["REACT_APP_API_URL"] = "http://localhost:8000"
        
        # Launch React development server
        subprocess.run(["npm", "start"], cwd=frontend_dir, env=env)
    except KeyboardInterrupt:
        print("\n👋 Shutting down the React server...")
    except FileNotFoundError:
        print("❌ npm not found. Please install Node.js and npm first.")
        print("Visit: https://nodejs.org/")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error launching React server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
