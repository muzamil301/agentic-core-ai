#!/usr/bin/env python3
"""
Start both API and HTML frontend servers.

This launches the complete application with the HTML frontend.
"""

import subprocess
import sys
import time
import signal
from pathlib import Path
from threading import Thread


class HTMLAppLauncher:
    def __init__(self):
        self.api_process = None
        self.frontend_process = None
        self.running = True
    
    def start_api_server(self):
        """Start the API server."""
        print("🔧 Starting API Server...")
        api_dir = Path(__file__).parent / "api"
        
        try:
            self.api_process = subprocess.Popen([
                sys.executable, "simple_main.py"
            ], cwd=api_dir)
            
            print(f"✅ API Server started (PID: {self.api_process.pid})")
            return True
        except Exception as e:
            print(f"❌ Failed to start API server: {e}")
            return False
    
    def start_frontend_server(self):
        """Start the HTML frontend server."""
        print("🌐 Starting HTML Frontend Server...")
        
        try:
            self.frontend_process = subprocess.Popen([
                sys.executable, "serve_frontend.py"
            ])
            
            print(f"✅ Frontend Server started (PID: {self.frontend_process.pid})")
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
            print("🌐 Frontend Server stopped")
    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C signal."""
        self.stop_servers()
        sys.exit(0)
    
    def run(self):
        """Run the complete HTML application."""
        print("🚀 Starting HTML Chat Application")
        print("=" * 60)
        
        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # Start API server
        if not self.start_api_server():
            return
        
        # Wait for API server to start
        print("⏳ Waiting for API server to initialize...")
        time.sleep(3)
        
        # Start frontend server
        if not self.start_frontend_server():
            self.stop_servers()
            return
        
        print("\n" + "=" * 60)
        print("✅ HTML Chat Application Started Successfully!")
        print("🔗 API Server: http://localhost:8000")
        print("🌐 Frontend: http://localhost:3000/simple_frontend.html")
        print("📖 API Docs: http://localhost:8000/docs")
        print("\n🌐 Browser should open automatically...")
        print("🛑 Press Ctrl+C to stop both servers")
        print("=" * 60)
        
        # Keep the main process running
        try:
            while self.running:
                time.sleep(1)
                
                # Check if processes are still running
                if self.api_process and self.api_process.poll() is not None:
                    print("❌ API server stopped unexpectedly")
                    break
                
                if self.frontend_process and self.frontend_process.poll() is not None:
                    print("❌ Frontend server stopped unexpectedly")
                    break
        
        except KeyboardInterrupt:
            self.stop_servers()


def main():
    """Main function."""
    print("🎯 HTML Chat Application Launcher")
    print("This starts both API and HTML frontend servers")
    print("")
    
    launcher = HTMLAppLauncher()
    launcher.run()


if __name__ == "__main__":
    main()
