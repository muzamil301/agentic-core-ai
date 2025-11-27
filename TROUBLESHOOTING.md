# Troubleshooting Guide

## Issues with `python start_full_stack.py`

### Issue 1: `ModuleNotFoundError: No module named 'langgraph.graph.message'`

**Problem**: LangGraph import path has changed in newer versions.

**Solution**: The import has been fixed in `langgraph/graph/state.py`. If you still see this error:

```bash
# Try installing a specific LangGraph version
pip install langgraph==0.2.0

# Or update to latest
pip install --upgrade langgraph
```

### Issue 2: npm cache permission errors

**Problem**: npm cache has permission issues.

**Solutions**:

#### Option A: Use the fixed launcher
```bash
python fix_and_start.py
```

#### Option B: Manual fix
```bash
# Clear npm cache
npm cache clean --force

# Fix permissions (macOS/Linux)
sudo chown -R $(whoami) ~/.npm

# Or use different npm cache directory
npm config set cache ~/.npm-cache

# Then try again
python start_full_stack.py
```

#### Option C: Use yarn instead of npm
```bash
# Install yarn
npm install -g yarn

# In frontend directory
cd frontend
yarn install
yarn start
```

### Issue 3: Port conflicts

**Problem**: Ports 3000 or 8000 are already in use.

**Solution**:
```bash
# Check what's using the ports
lsof -i :3000
lsof -i :8000

# Kill processes if needed
kill -9 <PID>

# Or use different ports
# For API (edit api/main.py):
uvicorn.run(app, host="0.0.0.0", port=8001)

# For React (edit frontend/package.json):
"start": "PORT=3001 react-scripts start"
```

## Alternative Launch Methods

### Method 1: Fixed Launcher (Recommended)
```bash
python fix_and_start.py
```

### Method 2: Step-by-step manual launch

#### Step 1: Start API server
```bash
cd api
python simple_main.py
# Should show: "RAG Chat API server running on http://localhost:8000"
```

#### Step 2: Install frontend dependencies (in new terminal)
```bash
cd frontend
npm cache clean --force
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

#### Step 3: Start frontend (same terminal)
```bash
npm start
# Should open http://localhost:3000
```

### Method 3: Individual components

#### API only:
```bash
cd api && python simple_main.py
```

#### Frontend only (after API is running):
```bash
cd frontend && npm start
```

#### Streamlit UI (alternative):
```bash
python langgraph/run_ui.py
```

## Common Issues & Solutions

### 1. "RAG service not available"

**Symptoms**: API starts but shows "RAG service not available" message.

**Causes & Solutions**:

#### Missing Ollama
```bash
# Install Ollama
# Visit: https://ollama.ai

# Pull a chat model
ollama pull llama3.2
# or
ollama pull mistral

# Verify Ollama is running
curl http://localhost:11434/api/tags
```

#### Missing ChromaDB embeddings
```bash
# Create embeddings
python embeddings-management/scripts/payment_support_embeddings.py

# Verify embeddings exist
python embeddings-management/scripts/read_embeddings.py
```

#### Missing dependencies
```bash
pip install -r requirements.txt
```

### 2. Frontend won't connect to API

**Symptoms**: Frontend loads but can't send messages.

**Solutions**:

#### Check API is running
```bash
curl http://localhost:8000/status
```

#### Check CORS settings
In `api/main.py`, verify:
```python
allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"]
```

#### Check proxy settings
In `frontend/package.json`:
```json
"proxy": "http://localhost:8000"
```

### 3. Node.js/npm issues

#### Install Node.js
```bash
# Visit: https://nodejs.org/
# Download and install LTS version

# Verify installation
node --version  # Should show v16+
npm --version   # Should show v8+
```

#### Fix npm permissions (macOS/Linux)
```bash
# Option 1: Change npm's default directory
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.profile
source ~/.profile

# Option 2: Fix current permissions
sudo chown -R $(whoami) ~/.npm
```

#### Use nvm (Node Version Manager)
```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Install and use Node.js LTS
nvm install --lts
nvm use --lts
```

### 4. Python import errors

#### Path issues
Make sure you're running from the project root:
```bash
cd /path/to/embeddings-py
python fix_and_start.py
```

#### Virtual environment
```bash
# Create virtual environment
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 5. Performance issues

#### Slow responses
- First query is always slower (model loading)
- Check Ollama model size (smaller models are faster)
- Ensure sufficient RAM (8GB+ recommended)

#### High CPU usage
- Use smaller Ollama models
- Reduce `RETRIEVAL_TOP_K` in settings
- Close other applications

## Testing Individual Components

### Test Ollama
```bash
curl -X POST http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3.2", "messages": [{"role": "user", "content": "Hello"}]}'
```

### Test ChromaDB
```bash
python -c "
from db.chromadb_service import ChromaDBService
db = ChromaDBService('payment_support')
print(db.get_info())
"
```

### Test RAG Service
```bash
python -c "
from langgraph.service.rag_service import RAGService
service = RAGService()
result = service.chat('Hello')
print(result)
"
```

### Test API
```bash
# Start API
cd api && python simple_main.py

# In another terminal, test
curl http://localhost:8000/status
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

## Getting Help

### Check logs
- **API logs**: Look at terminal where API is running
- **Frontend logs**: Check browser console (F12)
- **Ollama logs**: Check Ollama service logs

### Debug mode
```bash
# API with debug
cd api && python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from simple_main import app
import uvicorn
uvicorn.run(app, host='0.0.0.0', port=8000, log_level='debug')
"

# Frontend with verbose
cd frontend && npm start --verbose
```

### System requirements
- **Python**: 3.8+
- **Node.js**: 16+
- **RAM**: 8GB+ (for Ollama models)
- **Storage**: 5GB+ (for models and embeddings)
- **OS**: macOS, Linux, Windows

---

## Quick Fix Summary

If you're having issues, try this sequence:

1. **Use the fixed launcher**:
   ```bash
   python fix_and_start.py
   ```

2. **If that fails, manual approach**:
   ```bash
   # Terminal 1: API
   cd api && python simple_main.py
   
   # Terminal 2: Frontend
   cd frontend
   npm cache clean --force
   rm -rf node_modules
   npm install --legacy-peer-deps
   npm start
   ```

3. **If still failing, check prerequisites**:
   - Ollama running with chat model
   - ChromaDB with embeddings
   - Node.js and npm installed
   - All Python dependencies installed

4. **Alternative UI**:
   ```bash
   # Use Streamlit instead of React
   python langgraph/run_ui.py
   ```

Most issues are resolved by the fixed launcher or manual step-by-step approach! 🎯
