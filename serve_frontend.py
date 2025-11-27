#!/usr/bin/env python3
"""
Simple HTTP server to serve the HTML frontend.

This fixes CORS issues by serving the HTML file over HTTP instead of file://.
"""

import http.server
import socketserver
import webbrowser
import threading
import time
from pathlib import Path


def start_server():
    """Start a simple HTTP server for the frontend."""
    port = 3000
    handler = http.server.SimpleHTTPRequestHandler
    
    # Change to the directory containing the HTML file
    frontend_dir = Path(__file__).parent
    import os
    os.chdir(frontend_dir)
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"🌐 Frontend server running at: http://localhost:{port}")
            print(f"📄 Serving: simple_frontend.html")
            print(f"🔗 Make sure API is running at: http://localhost:8000")
            print(f"🛑 Press Ctrl+C to stop")
            
            # Open browser after a short delay
            def open_browser():
                time.sleep(1)
                webbrowser.open(f"http://localhost:{port}/simple_frontend.html")
            
            threading.Thread(target=open_browser, daemon=True).start()
            
            httpd.serve_forever()
            
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use")
            print("Try stopping other servers or use a different port")
        else:
            print(f"❌ Error starting server: {e}")


if __name__ == "__main__":
    print("🚀 Starting Frontend HTTP Server...")
    start_server()
