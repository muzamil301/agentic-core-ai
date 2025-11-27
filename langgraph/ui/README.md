# Web UI for RAG Chat Application

This directory contains the web-based user interface for the RAG chat application.

## Components

### `streamlit_app.py`
Main Streamlit application providing:
- **Modern Chat Interface**: Clean, responsive web UI
- **Real-time Messaging**: Interactive chat with the RAG service
- **Conversation History**: Persistent chat history within session
- **Response Metadata**: Shows retrieval details and response metrics
- **Example Queries**: Pre-built queries for easy testing
- **Service Status**: Real-time service health monitoring

## Features

### 🎨 User Interface
- **Responsive Design**: Works on desktop and mobile
- **Modern Styling**: Custom CSS for professional appearance
- **Message Threading**: Clear distinction between user and assistant messages
- **Sidebar Controls**: Easy access to settings and examples

### 🤖 Smart Routing
- **Intelligent Classification**: Automatically determines if queries need RAG or direct answers
- **Query Types**:
  - **RAG Required**: Payment-specific questions using knowledge base
  - **Direct Answer**: General questions answered directly by LLM
  - **Greetings**: Friendly responses to social interactions
  - **Unclear**: Ambiguous queries handled gracefully

### 📊 Observability
- **Response Metadata**: Shows classification confidence, retrieval count, response time
- **Service Status**: Real-time monitoring of RAG service health
- **Conversation Metrics**: Track conversation length and turns

## Usage

### Launch Web UI

```bash
# From project root
python langgraph/run_ui.py

# Or directly with streamlit
streamlit run langgraph/ui/streamlit_app.py
```

### Access the Application
- **URL**: http://localhost:8501
- **Auto-open**: Browser opens automatically
- **Mobile**: Responsive design works on mobile devices

### Example Interactions

#### Payment Questions (RAG)
- "What is my daily transaction limit?"
- "How do I block my card?"
- "How long do international transfers take?"

#### General Questions (Direct)
- "Hello, how are you?"
- "What's the weather like?"
- "Tell me a joke"

#### System Features
- **Reset Conversation**: Clear chat history
- **Example Queries**: Click sidebar examples
- **Response Details**: Expand metadata sections

## Architecture

### Flow Diagram
```
User Input → Streamlit UI → RAG Service → LangGraph → Response
    ↓
Query Classification → Route Decision
    ├─ RAG Path: Retrieve → Format → Generate
    └─ Direct Path: Direct Answer
```

### Integration Points
- **RAG Service**: Uses `langgraph.service.rag_service.RAGService`
- **Session State**: Manages conversation history in Streamlit
- **Error Handling**: Graceful degradation when services are unavailable

## Configuration

### Streamlit Settings
- **Port**: 8501 (default)
- **Auto-reload**: Enabled for development
- **Browser**: Opens automatically
- **Headless**: Disabled (shows in browser)

### Customization
- **Styling**: Modify CSS in `streamlit_app.py`
- **Layout**: Adjust columns and containers
- **Features**: Add new sidebar controls or metrics

## Development

### Local Development
```bash
# Install dependencies
pip install streamlit

# Run in development mode
streamlit run langgraph/ui/streamlit_app.py --server.runOnSave true
```

### Adding Features
1. **New UI Components**: Add to `streamlit_app.py`
2. **Custom Styling**: Modify CSS in `st.markdown()`
3. **New Metrics**: Add to sidebar metrics section
4. **Enhanced Routing**: Modify query classification logic

## Troubleshooting

### Common Issues

#### "RAG Service: Offline"
- Ensure Ollama is running with a chat model
- Check ChromaDB has embeddings stored
- Verify all dependencies are installed

#### "Module not found" errors
- Run from project root directory
- Check Python path includes parent directories
- Install missing dependencies: `pip install -r requirements.txt`

#### UI not loading
- Check port 8501 is available
- Try different port: `streamlit run app.py --server.port 8502`
- Check firewall settings

#### Slow responses
- Ollama model loading (first query is slower)
- Large ChromaDB collections
- Network latency to Ollama API

### Debug Mode
Enable debug information by setting environment variable:
```bash
export STREAMLIT_DEBUG=true
streamlit run langgraph/ui/streamlit_app.py
```

## Future Enhancements

### Planned Features
- **User Authentication**: Multi-user support
- **Chat Export**: Download conversation history
- **Theme Switching**: Light/dark mode toggle
- **Voice Input**: Speech-to-text integration
- **File Upload**: Document upload for RAG
- **Analytics Dashboard**: Usage statistics

### Technical Improvements
- **Streaming Responses**: Real-time response generation
- **Caching**: Response caching for common queries
- **Rate Limiting**: Prevent API abuse
- **Monitoring**: Application performance metrics
- **Testing**: Automated UI testing

## Security Considerations

- **Input Validation**: Sanitize user inputs
- **Rate Limiting**: Prevent excessive API calls
- **Error Handling**: Don't expose internal errors
- **HTTPS**: Use SSL in production
- **Authentication**: Add user authentication for production use

