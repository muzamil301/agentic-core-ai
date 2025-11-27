"""
Simple FastAPI server without uvicorn auto-reload to avoid import issues.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chat API",
    description="API for RAG-powered chat application",
    version="1.0.0"
)

# Configure CORS - Allow file:// and localhost origins
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
rag_service: Optional[Any] = None

# Pydantic models
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

# Initialize RAG service
def init_rag_service():
    """Initialize the RAG service with error handling."""
    global rag_service
    try:
        # Try the simple RAG service first (more reliable)
        from langgraph.service.simple_rag_service import SimpleRAGService
        rag_service = SimpleRAGService()
        print("✅ Simple RAG service initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize simple RAG service: {e}")
        try:
            # Fallback to full RAG service
            from langgraph.service.rag_service import RAGService
            rag_service = RAGService()
            print("✅ Full RAG service initialized successfully")
            return True
        except Exception as e2:
            print(f"❌ Failed to initialize full RAG service: {e2}")
            print("⚠️  API will run in limited mode")
            rag_service = None
            return False

@app.on_event("startup")
async def startup_event():
    """Initialize the RAG service on application startup."""
    init_rag_service()

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "RAG Chat API",
        "version": "1.0.0",
        "status": "running",
        "rag_service_available": rag_service is not None
    }

@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Get the current status of the RAG service."""
    if rag_service is None:
        return StatusResponse(
            connected=False,
            service_status="disconnected",
            message="RAG service is not initialized. Check Ollama and ChromaDB."
        )
    
    return StatusResponse(
        connected=True,
        service_status="connected",
        message="RAG service is running and responsive"
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message to the RAG service and get a response."""
    if rag_service is None:
        # Fallback response when RAG service is not available
        return ChatResponse(
            response="I'm sorry, the RAG service is currently unavailable. Please check that Ollama is running and ChromaDB has embeddings stored.",
            metadata={"error": "RAG service not available"}
        )
    
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        result = rag_service.chat(
            query=request.message,
            reset_history=request.reset_history
        )
        
        return ChatResponse(
            response=result.get("response", ""),
            metadata=result.get("metadata", {})
        )
    
    except Exception as e:
        return ChatResponse(
            response=f"I encountered an error: {str(e)}",
            metadata={"error": str(e)}
        )

@app.post("/chat/reset")
async def reset_conversation():
    """Reset the conversation history."""
    if rag_service is None:
        return {"message": "RAG service not available"}
    
    try:
        rag_service.reset_conversation()
        return {"message": "Conversation reset successfully"}
    except Exception as e:
        return {"message": f"Error resetting conversation: {str(e)}"}

@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {
        "status": "healthy",
        "service": "rag-chat-api",
        "rag_service_available": rag_service is not None
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting RAG Chat API server...")
    print("📱 Frontend should connect to: http://localhost:8000")
    print("📖 API docs available at: http://localhost:8000/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
