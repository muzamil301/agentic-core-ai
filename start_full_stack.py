#!/usr/bin/env python3
"""
Full Stack Launcher for RAG Chat Application

This script starts both the FastAPI backend and React frontend.
"""

import subprocess
import sys
import time
import signal
from pathlib import Path
from threading import Thread


class FullStackLauncher:
    def __init__(self):
        self.api_process = None
        self.frontend_process = None
        self.running = True
    
    def start_api_server(self):
        """Start the FastAPI backend server."""
        print("🔧 Starting API Server...")
        api_dir = Path(__file__).parent / "api"
        
        try:
            self.api_process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", "main:app",
                "--host", "0.0.0.0",
                "--port", "8000",
                "--reload"
            ], cwd=api_dir)
            
            print("✅ API Server started (PID: {})".format(self.api_process.pid))
            return True
        except Exception as e:
            print(f"❌ Failed to start API server: {e}")
            return False
    
    def start_frontend_server(self):
        """Start the React frontend server."""
        print("🎨 Starting Frontend Server...")
        frontend_dir = Path(__file__).parent / "frontend"
        
        # Check if dependencies are installed
        node_modules = frontend_dir / "node_modules"
        if not node_modules.exists():
            print("📦 Installing frontend dependencies...")
            try:
                subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install dependencies: {e}")
                return False
        
        try:
            # Set environment variables
            import os
            env = os.environ.copy()
            env["REACT_APP_API_URL"] = "http://localhost:8000"
            
            self.frontend_process = subprocess.Popen([
                "npm", "start"
            ], cwd=frontend_dir, env=env)
            
            print("✅ Frontend Server started (PID: {})".format(self.frontend_process.pid))
            return True
        except Exception as e:
            print(f"❌ Failed to start frontend server: {e}")
            return False
    
    def stop_servers(self):
        """Stop both servers."""
        print("\n🛑 Stopping servers...")
        self.running = False
        
        if self.api_process:
            self.api_process.terminate()
            print("🔧 API Server stopped")
        
        if self.frontend_process:
            self.frontend_process.terminate()
            print("🎨 Frontend Server stopped")
    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C signal."""
        self.stop_servers()
        sys.exit(0)
    
    def run(self):
        """Run the full stack application."""
        print("🚀 Starting Full Stack RAG Chat Application")
        print("=" * 60)
        
        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # Start API server
        if not self.start_api_server():
            return
        
        # Wait a bit for API server to start
        print("⏳ Waiting for API server to initialize...")
        time.sleep(3)
        
        # Start frontend server
        if not self.start_frontend_server():
            self.stop_servers()
            return
        
        print("\n" + "=" * 60)
        print("✅ Full Stack Application Started Successfully!")
        print("🔗 API Server: http://localhost:8000")
        print("🌐 Frontend: http://localhost:3000")
        print("📖 API Docs: http://localhost:8000/docs")
        print("🛑 Press Ctrl+C to stop both servers")
        print("=" * 60)
        
        # Keep the main process running
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_servers()


def main():
    """Main function."""
    # Check prerequisites
    try:
        subprocess.run(["node", "--version"], capture_output=True, check=True)
        subprocess.run(["npm", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js and npm are required for the frontend.")
        print("Please install Node.js from: https://nodejs.org/")
        sys.exit(1)
    
    # Check if required directories exist
    api_dir = Path(__file__).parent / "api"
    frontend_dir = Path(__file__).parent / "frontend"
    
    if not api_dir.exists():
        print(f"❌ API directory not found: {api_dir}")
        sys.exit(1)
    
    if not frontend_dir.exists():
        print(f"❌ Frontend directory not found: {frontend_dir}")
        sys.exit(1)
    
    # Launch the application
    launcher = FullStackLauncher()
    launcher.run()


if __name__ == "__main__":
    main()
