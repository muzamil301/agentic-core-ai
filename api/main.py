"""
FastAPI Backend for RAG Chat Application

This API serves as a bridge between the React frontend and LangGraph RAG service.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import sys
from pathlib import Path
import uvicorn

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from langgraph.service.rag_service import RAGService

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chat API",
    description="API for RAG-powered chat application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "null"  # This allows file:// protocol
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global RAG service instance
rag_service: Optional[RAGService] = None

# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str
    reset_history: bool = False

class ChatResponse(BaseModel):
    response: str
    metadata: Dict[str, Any] = {}

class StatusResponse(BaseModel):
    connected: bool
    service_status: str
    message: str

class HistoryResponse(BaseModel):
    messages: list
    count: int

# Initialize RAG service on startup
@app.on_event("startup")
async def startup_event():
    """Initialize the RAG service on application startup."""
    global rag_service
    try:
        rag_service = RAGService()
        print("✅ RAG service initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize RAG service: {e}")
        rag_service = None

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "RAG Chat API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "chat": "/chat",
            "status": "/status",
            "reset": "/chat/reset",
            "history": "/chat/history"
        }
    }

@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Get the current status of the RAG service."""
    if rag_service is None:
        return StatusResponse(
            connected=False,
            service_status="disconnected",
            message="RAG service is not initialized. Please check Ollama and ChromaDB."
        )
    
    try:
        # Test the service with a simple query
        test_result = rag_service.chat("test", reset_history=True)
        return StatusResponse(
            connected=True,
            service_status="connected",
            message="RAG service is running and responsive"
        )
    except Exception as e:
        return StatusResponse(
            connected=False,
            service_status="error",
            message=f"RAG service error: {str(e)}"
        )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message to the RAG service and get a response."""
    if rag_service is None:
        raise HTTPException(
            status_code=503,
            detail="RAG service is not available. Please check the service status."
        )
    
    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )
    
    try:
        # Call the RAG service
        result = rag_service.chat(
            query=request.message,
            reset_history=request.reset_history
        )
        
        return ChatResponse(
            response=result.get("response", ""),
            metadata=result.get("metadata", {})
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )

@app.post("/chat/reset")
async def reset_conversation():
    """Reset the conversation history."""
    if rag_service is None:
        raise HTTPException(
            status_code=503,
            detail="RAG service is not available"
        )
    
    try:
        rag_service.reset_conversation()
        return {"message": "Conversation reset successfully"}
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error resetting conversation: {str(e)}"
        )

@app.get("/chat/history", response_model=HistoryResponse)
async def get_conversation_history():
    """Get the current conversation history."""
    if rag_service is None:
        raise HTTPException(
            status_code=503,
            detail="RAG service is not available"
        )
    
    try:
        history = rag_service.get_conversation_history()
        return HistoryResponse(
            messages=history,
            count=len(history)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting conversation history: {str(e)}"
        )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {
        "status": "healthy",
        "service": "rag-chat-api",
        "rag_service_available": rag_service is not None
    }

if __name__ == "__main__":
    print("🚀 Starting RAG Chat API server...")
    print("📱 Frontend should connect to: http://localhost:8000")
    print("📖 API docs available at: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop the server")
    
    # Use simple uvicorn run without reload to avoid import issues
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
