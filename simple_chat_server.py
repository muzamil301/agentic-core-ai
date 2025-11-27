#!/usr/bin/env python3
"""
Simple chat server that works without FastAPI/Pydantic dependencies.

This uses only Python standard library and basic HTTP server.
"""

import json
import http.server
import socketserver
import urllib.parse
from pathlib import Path
import sys
import threading
import webbrowser
import time

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


class ChatHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler for the chat API."""
    
    def __init__(self, *args, **kwargs):
        # Initialize RAG service
        self.rag_service = None
        self._init_rag_service()
        super().__init__(*args, **kwargs)
    
    def _init_rag_service(self):
        """Initialize RAG service with fallbacks."""
        try:
            from langgraph.service.simple_rag_service import SimpleRAGService
            self.rag_service = SimpleRAGService()
            print("✅ Simple RAG service initialized")
        except Exception as e:
            print(f"⚠️  RAG service failed: {e}")
            self.rag_service = None
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests."""
        self._set_cors_headers()
        
        if self.path == '/':
            self._handle_root()
        elif self.path == '/status':
            self._handle_status()
        elif self.path == '/health':
            self._handle_health()
        else:
            self._handle_404()
    
    def do_POST(self):
        """Handle POST requests."""
        self._set_cors_headers()
        
        if self.path == '/chat':
            self._handle_chat()
        else:
            self._handle_404()
    
    def _set_cors_headers(self):
        """Set CORS headers."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def _send_json_response(self, data, status_code=200):
        """Send JSON response."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self._set_cors_headers()
        self.end_headers()
        
        json_data = json.dumps(data, indent=2)
        self.wfile.write(json_data.encode('utf-8'))
    
    def _handle_root(self):
        """Handle root endpoint."""
        response = {
            "message": "Simple RAG Chat API",
            "version": "1.0.0",
            "status": "running",
            "rag_service_available": self.rag_service is not None
        }
        self._send_json_response(response)
    
    def _handle_status(self):
        """Handle status endpoint."""
        response = {
            "connected": self.rag_service is not None,
            "service_status": "connected" if self.rag_service else "disconnected",
            "message": "RAG service is ready" if self.rag_service else "RAG service is not initialized"
        }
        self._send_json_response(response)
    
    def _handle_health(self):
        """Handle health endpoint."""
        response = {
            "status": "healthy",
            "rag_service_available": self.rag_service is not None,
            "timestamp": time.time()
        }
        self._send_json_response(response)
    
    def _handle_chat(self):
        """Handle chat endpoint."""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # Parse JSON
            try:
                data = json.loads(post_data.decode('utf-8'))
            except json.JSONDecodeError:
                self._send_json_response({"error": "Invalid JSON"}, 400)
                return
            
            message = data.get('message', '').strip()
            reset_history = data.get('reset_history', False)
            
            if not message:
                self._send_json_response({"error": "Message is required"}, 400)
                return
            
            # Process with RAG service
            if self.rag_service:
                try:
                    result = self.rag_service.chat(message, reset_history)
                    self._send_json_response(result)
                except Exception as e:
                    error_response = {
                        "response": f"I encountered an error: {str(e)}",
                        "metadata": {"error": str(e), "service_type": "error"}
                    }
                    self._send_json_response(error_response)
            else:
                # Fallback response
                fallback_response = {
                    "response": "I'm sorry, the RAG service is currently unavailable. This is a simple fallback response.",
                    "metadata": {"service_type": "fallback", "error": "RAG service not available"}
                }
                self._send_json_response(fallback_response)
        
        except Exception as e:
            error_response = {
                "response": f"Server error: {str(e)}",
                "metadata": {"error": str(e), "service_type": "server_error"}
            }
            self._send_json_response(error_response, 500)
    
    def _handle_404(self):
        """Handle 404 errors."""
        self._send_json_response({"error": "Not found"}, 404)
    
    def log_message(self, format, *args):
        """Override to reduce logging noise."""
        pass


def start_server(port=8000):
    """Start the simple chat server."""
    handler = ChatHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"🚀 Simple Chat Server Started")
            print(f"🔗 Server: http://localhost:{port}")
            print(f"📄 Status: http://localhost:{port}/status")
            print(f"💬 Chat: POST to http://localhost:{port}/chat")
            print(f"🛑 Press Ctrl+C to stop")
            print("=" * 50)
            
            # Start server
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use")
            print("Try stopping other servers or use a different port")
        else:
            print(f"❌ Error starting server: {e}")


def main():
    """Main function."""
    print("🎯 Simple Chat Server")
    print("This is a lightweight alternative to FastAPI")
    print("")
    
    start_server()


if __name__ == "__main__":
    main()
