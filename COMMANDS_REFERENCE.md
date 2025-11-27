# 📋 Commands Reference Guide

**Quick reference for all commands to run the RAG Chat System**

## 🚀 **Quick Start Commands**

### **Option 1: Streamlit UI** ⭐ *Recommended*
```bash
python langgraph/run_ui.py
```
- **URL**: http://localhost:8501
- **Features**: Full RAG functionality, conversation history, real-time chat
- **Best for**: Complete RAG experience with all features

### **Option 2: Standalone HTML Demo**
```bash
open standalone_chat.html
# Or double-click the file in Finder
```
- **Features**: Beautiful UI, simulated responses, no setup required
- **Best for**: Quick demo, UI showcase, offline use

### **Option 3: CLI Chat**
```bash
python langgraph/chat.py
```
- **Features**: Terminal-based chat, full RAG functionality
- **Best for**: Developers, debugging, headless environments

## 🔧 **Setup Commands**

### **Initial Setup**
```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Start Ollama (in separate terminal)
ollama serve

# 3. Download required models
ollama pull llama3.2
ollama pull all-minilm

# 4. Create embeddings (if not exists)
python embeddings-management/scripts/payment_support_embeddings.py
```

### **Verify Setup**
```bash
# Check Ollama models
ollama list

# Check embeddings
python embeddings-management/scripts/read_embeddings.py

# Test RAG service
python test_simple_chat.py

# Run diagnostics
python debug_connection.py
```

## 🌐 **Server Commands**

### **API Servers**

#### **FastAPI Server** (Full Features)
```bash
python start_api_only.py
```
- **URL**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Features**: WebSocket, REST API, full functionality

#### **Simple API Server** (Lightweight)
```bash
cd api
python simple_main.py
```
- **URL**: http://localhost:8000
- **Features**: Basic REST API, reduced dependencies

#### **Pure Python Server** (No Dependencies)
```bash
python simple_chat_server.py
```
- **URL**: http://localhost:8000
- **Features**: Standard library only, maximum compatibility

### **Frontend Servers**

#### **React Development Server**
```bash
cd frontend
npm install
npm start
```
- **URL**: http://localhost:3000
- **Features**: Hot reload, modern React interface

#### **HTML File Server**
```bash
python serve_frontend.py
```
- **URL**: http://localhost:3000/simple_frontend.html
- **Features**: Serves HTML files over HTTP (fixes CORS)

### **Combined Launchers**

#### **Full Stack** (API + React)
```bash
python start_full_stack.py
```
- **API**: http://localhost:8000
- **Frontend**: http://localhost:3000

#### **HTML Stack** (API + HTML)
```bash
python start_html_app.py
```
- **API**: http://localhost:8000
- **Frontend**: http://localhost:3000/simple_frontend.html

## 🔍 **Debugging Commands**

### **Connection Testing**
```bash
# Test API connectivity
python debug_connection.py

# Test RAG service directly
python test_simple_chat.py

# Check API status
curl http://localhost:8000/status

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello test"}'
```

### **Process Management**
```bash
# Check running processes
ps aux | grep python
ps aux | grep ollama

# Check port usage
lsof -i :8000    # API port
lsof -i :8501    # Streamlit port
lsof -i :3000    # Frontend port
lsof -i :11434   # Ollama port

# Kill processes
kill -9 <PID>
```

### **System Diagnostics**
```bash
# Check Ollama status
ollama list
ollama ps

# Check Python environment
python --version
pip list | grep -E "(streamlit|fastapi|chromadb|langgraph)"

# Check disk space (ChromaDB)
du -sh chroma_db/
```

## 📊 **Embeddings Management**

### **Create/Update Embeddings**
```bash
# Create payment support embeddings
python embeddings-management/scripts/payment_support_embeddings.py

# Read existing embeddings
python embeddings-management/scripts/read_embeddings.py

# Get collection info
python embeddings-management/scripts/get_info.py

# Delete embeddings (careful!)
python embeddings-management/scripts/delete_embeddings.py
```

### **Test CRUD Operations**
```bash
# Run complete CRUD test
python embeddings-management/tests/test_complete_crud.py

# Test specific operations
python embeddings-management/examples/get_embeddings.py
```

## 🛠️ **Troubleshooting Commands**

### **Fix npm Issues** (macOS)
```bash
# Automated fix
python fix_npm_permissions.py

# Manual fix
sudo chown -R $(whoami) ~/.npm
npm cache clean --force
rm -rf frontend/node_modules frontend/package-lock.json
cd frontend && npm install --legacy-peer-deps
```

### **Fix Architecture Issues** (Apple Silicon)
```bash
# Reinstall packages for ARM64
pip uninstall numpy pydantic fastapi chromadb
pip install --no-cache-dir numpy pydantic fastapi chromadb

# Use Rosetta if needed
arch -x86_64 python langgraph/run_ui.py
```

### **Reset Everything**
```bash
# Stop all processes
pkill -f "python.*streamlit"
pkill -f "python.*fastapi"
pkill -f "python.*uvicorn"

# Clean caches
rm -rf __pycache__ */__pycache__ */*/__pycache__
rm -rf .streamlit/
npm cache clean --force

# Restart Ollama
pkill ollama
ollama serve
```

## 📱 **Usage Examples**

### **Example Chat Queries**

#### **RAG Queries** (Uses Knowledge Base)
```bash
# In any chat interface:
"What is my daily transaction limit?"
"How do I block my card?"
"How long do international transfers take?"
"Tell me about account tiers"
"What are the fees for wire transfers?"
```

#### **Direct Queries** (No RAG Needed)
```bash
"Hello, how are you?"
"What's 2+2?"
"Tell me a joke"
"What's the weather like?"
```

### **API Usage Examples**

#### **Chat Endpoint**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is my daily transaction limit?",
    "reset_history": false
  }'
```

#### **Status Check**
```bash
curl http://localhost:8000/status
curl http://localhost:8000/health
```

## 🔄 **Development Workflow**

### **Daily Development**
```bash
# 1. Start Ollama
ollama serve

# 2. Start development UI
python langgraph/run_ui.py

# 3. Make changes to code

# 4. Test changes
python test_simple_chat.py

# 5. Commit changes
git add .
git commit -m "Your changes"
```

### **Testing Workflow**
```bash
# 1. Run diagnostics
python debug_connection.py

# 2. Test embeddings
python embeddings-management/scripts/read_embeddings.py

# 3. Test RAG service
python test_simple_chat.py

# 4. Test UI
python langgraph/run_ui.py
```

## 🚀 **Deployment Commands**

### **Production Setup**
```bash
# 1. Install production dependencies
pip install -r requirements.txt

# 2. Set environment variables
export OLLAMA_BASE_URL="http://localhost:11434"
export CHROMADB_PERSIST_DIRECTORY="./chroma_db"

# 3. Create embeddings
python embeddings-management/scripts/payment_support_embeddings.py

# 4. Start services
python langgraph/run_ui.py
```

### **Docker Commands** (Future)
```bash
# Build image
docker build -t rag-chat .

# Run container
docker run -p 8501:8501 rag-chat

# Docker compose
docker-compose up -d
```

## 📋 **Command Cheat Sheet**

| Purpose | Command | URL |
|---------|---------|-----|
| **Quick Start** | `python langgraph/run_ui.py` | http://localhost:8501 |
| **Demo** | `open standalone_chat.html` | Local file |
| **CLI Chat** | `python langgraph/chat.py` | Terminal |
| **API Only** | `python start_api_only.py` | http://localhost:8000 |
| **Full Stack** | `python start_full_stack.py` | Multiple ports |
| **Debug** | `python debug_connection.py` | Terminal output |
| **Test RAG** | `python test_simple_chat.py` | Terminal output |
| **Check Status** | `curl localhost:8000/status` | JSON response |

## 🆘 **Emergency Commands**

### **If Nothing Works**
```bash
# 1. Kill everything
pkill -f python
pkill ollama

# 2. Restart Ollama
ollama serve

# 3. Use Streamlit (most reliable)
python langgraph/run_ui.py

# 4. If that fails, use standalone demo
open standalone_chat.html
```

### **If Streamlit Fails**
```bash
# Try different port
streamlit run langgraph/ui/streamlit_app.py --server.port 8502

# Or use CLI
python langgraph/chat.py
```

### **If Everything Fails**
```bash
# Use the standalone demo (always works)
open standalone_chat.html
```

---

## 🎯 **Most Common Commands**

**For daily use, you'll mostly need these:**

```bash
# Start the system
ollama serve                    # Terminal 1
python langgraph/run_ui.py     # Terminal 2

# Quick demo
open standalone_chat.html

# Debug issues
python debug_connection.py
```

**That's it!** 🚀

---

*Keep this reference handy - it contains every command you'll need to run your RAG chat system!*
