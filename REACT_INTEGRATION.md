# React + LangGraph Integration

Complete React frontend with FastAPI backend integration for the RAG chat application.

## 🏗️ Architecture

```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐    Python    ┌─────────────────┐
│   React App     │ ◄──────────────► │   FastAPI       │ ◄───────────► │   LangGraph     │
│   (Frontend)    │                  │   (Backend)     │               │   RAG Service   │
│   Port: 3000    │                  │   Port: 8000    │               │                 │
└─────────────────┘                  └─────────────────┘               └─────────────────┘
```

## 📁 Project Structure

```
embeddings-py/
├── frontend/                    # 🎨 React Frontend
│   ├── src/
│   │   ├── components/
│   │   │   └── ChatMessage.js   # Message component
│   │   ├── services/
│   │   │   └── chatService.js   # API client
│   │   ├── styles/
│   │   │   ├── App.css          # Main styles
│   │   │   └── index.css        # Global styles
│   │   ├── App.js               # Main React component
│   │   └── index.js             # React entry point
│   ├── public/
│   │   └── index.html           # HTML template
│   ├── package.json             # Dependencies
│   └── run_frontend.py          # Frontend launcher
│
├── api/                         # 🔧 FastAPI Backend
│   ├── main.py                  # FastAPI application
│   ├── run_api.py               # API launcher
│   └── __init__.py
│
├── start_full_stack.py          # 🚀 Full stack launcher
└── requirements.txt             # Updated with API deps
```

## 🚀 Quick Start

### Prerequisites
1. **Node.js & npm** (for React frontend)
   ```bash
   # Install from https://nodejs.org/
   node --version  # Should show v16+ 
   npm --version   # Should show v8+
   ```

2. **Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Services running**
   - Ollama with chat model (e.g., `llama3.2`)
   - ChromaDB with embeddings (run `embeddings-management/scripts/payment_support_embeddings.py`)

### Launch Options

#### Option 1: Full Stack (Recommended)
```bash
# Starts both API and React servers
python start_full_stack.py
```
- API: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

#### Option 2: Separate Servers
```bash
# Terminal 1: Start API server
python api/run_api.py

# Terminal 2: Start React server  
python frontend/run_frontend.py
```

#### Option 3: Manual
```bash
# Terminal 1: API
cd api && python main.py

# Terminal 2: Frontend
cd frontend && npm install && npm start
```

## 🎨 React Frontend Features

### Modern UI Components
- **Responsive Design**: Works on desktop and mobile
- **Real-time Chat**: Instant message updates
- **Message History**: Persistent conversation within session
- **Typing Indicators**: Shows when AI is thinking
- **Example Queries**: Pre-built questions in sidebar

### Smart Features
- **Connection Status**: Shows API connectivity
- **Response Metadata**: Expandable details showing routing decisions
- **Error Handling**: Graceful error messages
- **Loading States**: Visual feedback during processing

### Component Structure
```jsx
App.js                          // Main application
├── ChatMessage.js             // Individual message component
├── Sidebar                    // Example queries & info
├── Chat Container             // Messages area
└── Input Form                 // Message input & send
```

## 🔧 FastAPI Backend Features

### REST API Endpoints
- `POST /chat` - Send message and get response
- `GET /status` - Check service health
- `POST /chat/reset` - Reset conversation
- `GET /chat/history` - Get conversation history
- `GET /health` - Health check

### API Documentation
- **Interactive Docs**: http://localhost:8000/docs
- **OpenAPI Schema**: Auto-generated from code
- **Request/Response Models**: Pydantic validation

### Error Handling
- **Service Unavailable**: When LangGraph is down
- **Validation Errors**: Invalid request format
- **Timeout Handling**: Long-running requests
- **CORS Configuration**: Allows React frontend

## 🔄 Data Flow

### Chat Message Flow
```
1. User types message in React
2. React calls POST /chat via chatService
3. FastAPI receives request
4. FastAPI calls RAGService.chat()
5. LangGraph processes (classify → route → respond)
6. Response flows back: LangGraph → FastAPI → React
7. React displays response with metadata
```

### Request/Response Format
```javascript
// Request
{
  "message": "What is my daily transaction limit?",
  "reset_history": false
}

// Response  
{
  "response": "Your daily transaction limit depends on...",
  "metadata": {
    "query_type": "rag_required",
    "classification_confidence": 0.85,
    "retrieval_count": 3,
    "response_time": 1.23
  }
}
```

## 🎯 Key Features

### Intelligent Routing Display
The React UI shows how queries are routed:
- **RAG Required**: Payment questions → Uses knowledge base
- **Direct Answer**: General questions → LLM only  
- **Greeting**: Social interactions → Friendly responses

### Real-time Feedback
- **Connection Status**: Green/red indicator
- **Typing Animation**: Shows AI is processing
- **Response Metadata**: Expandable details
- **Error Messages**: Clear error communication

### User Experience
- **Example Queries**: Click to try pre-built questions
- **Conversation Reset**: Clear history button
- **Responsive Design**: Works on all screen sizes
- **Keyboard Shortcuts**: Enter to send messages

## 🛠️ Development

### Frontend Development
```bash
cd frontend
npm install
npm start           # Development server with hot reload
npm run build       # Production build
npm test           # Run tests
```

### Backend Development
```bash
cd api
python main.py      # Development server with auto-reload
# API docs at http://localhost:8000/docs
```

### Environment Variables
```bash
# Frontend (.env in frontend/)
REACT_APP_API_URL=http://localhost:8000

# Backend (optional)
API_HOST=0.0.0.0
API_PORT=8000
```

## 🔧 Configuration

### CORS Settings
```python
# api/main.py
allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"]
```

### API Timeouts
```javascript
// frontend/src/services/chatService.js
timeout: 30000  // 30 seconds
```

### Proxy Configuration
```json
// frontend/package.json
"proxy": "http://localhost:8000"
```

## 🧪 Testing

### Manual Testing
1. **Start full stack**: `python start_full_stack.py`
2. **Open browser**: http://localhost:3000
3. **Test scenarios**:
   - Payment questions → Should show RAG routing
   - General questions → Should show direct routing
   - Greetings → Should show friendly responses
   - Connection issues → Should show error states

### API Testing
```bash
# Test API directly
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is my daily limit?"}'

# Check status
curl http://localhost:8000/status
```

### Frontend Testing
```bash
cd frontend
npm test            # Run React tests
npm run test:e2e    # End-to-end tests (if configured)
```

## 🚀 Deployment

### Production Build
```bash
# Frontend
cd frontend && npm run build

# Backend  
cd api && pip install -r requirements.txt
```

### Docker (Optional)
```dockerfile
# Example Dockerfile for API
FROM python:3.9
COPY api/ /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔍 Troubleshooting

### Common Issues

#### "Connection refused" errors
- Check if API server is running on port 8000
- Verify CORS settings allow frontend origin
- Check firewall/network settings

#### "RAG service not available"
- Ensure Ollama is running with chat model
- Check ChromaDB has embeddings stored
- Verify Python dependencies installed

#### Frontend won't start
- Install Node.js and npm
- Run `npm install` in frontend directory
- Check for port conflicts (3000)

#### API errors
- Check Python dependencies: `pip install -r requirements.txt`
- Verify LangGraph service can initialize
- Check logs for detailed error messages

### Debug Mode
```bash
# API with debug logging
cd api && python main.py --log-level debug

# Frontend with verbose output
cd frontend && npm start --verbose
```

## 📈 Performance

### Optimization Tips
- **API Response Caching**: Cache frequent queries
- **Frontend Optimization**: Use React.memo for components
- **Bundle Size**: Optimize React build for production
- **API Timeouts**: Adjust based on LLM response times

### Monitoring
- **API Metrics**: Response times, error rates
- **Frontend Metrics**: Load times, user interactions
- **LangGraph Metrics**: Query classification accuracy

## 🔮 Future Enhancements

### Planned Features
- **WebSocket Support**: Real-time streaming responses
- **File Upload**: Document upload for RAG
- **Voice Input**: Speech-to-text integration
- **Multi-language**: Internationalization support
- **User Authentication**: Multi-user support

### Technical Improvements
- **State Management**: Redux for complex state
- **Testing**: Comprehensive test suite
- **CI/CD**: Automated deployment pipeline
- **Monitoring**: Application performance monitoring

---

## ✅ Ready to Use!

The React + LangGraph integration is complete and ready for use:

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Install Node.js**: https://nodejs.org/
3. **Start services**: Ollama + ChromaDB with embeddings
4. **Launch app**: `python start_full_stack.py`
5. **Open browser**: http://localhost:3000

Enjoy your modern React-powered RAG chat application! 🎉
