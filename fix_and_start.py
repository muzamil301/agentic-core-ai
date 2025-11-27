#!/usr/bin/env python3
"""
Fixed launcher for RAG Chat Application

This script fixes common issues and starts the application.
"""

import subprocess
import sys
import os
import time
from pathlib import Path


def run_command(cmd, cwd=None, shell=False):
    """Run a command and return success status."""
    try:
        result = subprocess.run(cmd, cwd=cwd, shell=shell, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Command failed: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False


def fix_npm_cache():
    """Fix npm cache issues."""
    print("🔧 Fixing npm cache issues...")
    
    # Clear npm cache
    commands = [
        ["npm", "cache", "clean", "--force"],
        ["npm", "cache", "verify"]
    ]
    
    for cmd in commands:
        if not run_command(cmd):
            print("⚠️  Cache fix failed, but continuing...")
            break
    
    print("✅ npm cache fixed")


def install_frontend_deps():
    """Install frontend dependencies with fixes."""
    frontend_dir = Path(__file__).parent / "frontend"
    
    print("📦 Installing frontend dependencies...")
    
    # Remove existing node_modules and package-lock.json
    node_modules = frontend_dir / "node_modules"
    package_lock = frontend_dir / "package-lock.json"
    
    if node_modules.exists():
        print("🗑️  Removing old node_modules...")
        import shutil
        shutil.rmtree(node_modules)
    
    if package_lock.exists():
        print("🗑️  Removing package-lock.json...")
        package_lock.unlink()
    
    # Fix npm cache first
    fix_npm_cache()
    
    # Install with specific flags to avoid permission issues
    install_cmd = ["npm", "install", "--no-optional", "--legacy-peer-deps"]
    
    if not run_command(install_cmd, cwd=frontend_dir):
        print("⚠️  Standard install failed, trying alternative...")
        
        # Try with different flags
        alt_cmd = ["npm", "install", "--force", "--no-fund", "--no-audit"]
        if not run_command(alt_cmd, cwd=frontend_dir):
            print("❌ Frontend dependency installation failed")
            return False
    
    print("✅ Frontend dependencies installed")
    return True


def start_api_server():
    """Start the API server."""
    print("🔧 Starting API Server...")
    
    api_dir = Path(__file__).parent / "api"
    
    # Start with simpler command to avoid uvicorn issues
    try:
        process = subprocess.Popen([
            sys.executable, "main.py"
        ], cwd=api_dir)
        
        print(f"✅ API Server started (PID: {process.pid})")
        return process
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")
        return None


def start_frontend_server():
    """Start the frontend server."""
    print("🎨 Starting Frontend Server...")
    
    frontend_dir = Path(__file__).parent / "frontend"
    
    try:
        # Set environment variables
        env = os.environ.copy()
        env["REACT_APP_API_URL"] = "http://localhost:8000"
        env["BROWSER"] = "none"  # Don't auto-open browser
        
        process = subprocess.Popen([
            "npm", "start"
        ], cwd=frontend_dir, env=env)
        
        print(f"✅ Frontend Server started (PID: {process.pid})")
        return process
    except Exception as e:
        print(f"❌ Failed to start frontend server: {e}")
        return None


def main():
    """Main function."""
    print("🚀 Fixed RAG Chat Application Launcher")
    print("=" * 60)
    
    # Check Node.js
    if not run_command(["node", "--version"]):
        print("❌ Node.js not found. Please install from: https://nodejs.org/")
        return
    
    # Install frontend dependencies
    if not install_frontend_deps():
        print("❌ Cannot continue without frontend dependencies")
        return
    
    # Start API server
    api_process = start_api_server()
    if not api_process:
        return
    
    # Wait for API to start
    print("⏳ Waiting for API server to initialize...")
    time.sleep(5)
    
    # Start frontend server
    frontend_process = start_frontend_server()
    if not frontend_process:
        if api_process:
            api_process.terminate()
        return
    
    print("\n" + "=" * 60)
    print("✅ Application Started Successfully!")
    print("🔗 API Server: http://localhost:8000")
    print("🌐 Frontend: http://localhost:3000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("\n⏳ Waiting for frontend to compile...")
    print("🌐 Frontend will open automatically when ready")
    print("🛑 Press Ctrl+C to stop both servers")
    print("=" * 60)
    
    try:
        # Wait for processes
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if api_process.poll() is not None:
                print("❌ API server stopped unexpectedly")
                break
            
            if frontend_process.poll() is not None:
                print("❌ Frontend server stopped unexpectedly")
                break
    
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        
        if api_process:
            api_process.terminate()
            print("🔧 API Server stopped")
        
        if frontend_process:
            frontend_process.terminate()
            print("🎨 Frontend Server stopped")
        
        print("👋 Goodbye!")


if __name__ == "__main__":
    main()
