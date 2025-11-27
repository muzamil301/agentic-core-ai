# LangGraph + RAG Integration Plan: Chat Support App

## 📚 Table of Contents
1. [Understanding RAG (Retrieval Augmented Generation)](#understanding-rag)
2. [How LangGraph Fits In](#how-langgraph-fits-in)
3. [Architecture Overview](#architecture-overview)
4. [Implementation Plan](#implementation-plan)
5. [File Structure](#file-structure)
6. [Dependencies](#dependencies)
7. [Step-by-Step Implementation](#step-by-step-implementation)
8. [Testing Strategy](#testing-strategy)

---

## 🎯 Understanding RAG (Retrieval Augmented Generation)

### What is RAG?
RAG is a technique that enhances LLM responses by:
1. **Retrieving** relevant context from a knowledge base (your embeddings)
2. **Augmenting** the user's query with this context
3. **Generating** a response using both the query and retrieved context

### How RAG Works (Step-by-Step)

```
User Query: "What is my daily transaction limit?"
    ↓
1. QUERY EMBEDDING: Convert user query to embedding vector
    ↓
2. SEMANTIC SEARCH: Find similar embeddings in ChromaDB (vector similarity)
    ↓
3. RETRIEVAL: Get top-k most relevant documents (e.g., top 3)
    ↓
4. CONTEXT AUGMENTATION: Combine retrieved documents into context
    ↓
5. PROMPT CONSTRUCTION: Build prompt with:
   - System instructions
   - Retrieved context (knowledge base)
   - User query
    ↓
6. LLM GENERATION: Send to LLM (Ollama) to generate answer
    ↓
7. RESPONSE: Return natural language answer to user
```

### Why RAG?
- **Reduces Hallucination**: LLM uses actual data, not just training data
- **Up-to-date Information**: Knowledge base can be updated without retraining
- **Domain-Specific**: Works with your specific data (payment support)
- **Transparency**: Can cite sources from retrieved documents

---

## 🔗 How LangGraph Fits In

### What is LangGraph?
LangGraph is a framework for building **stateful, multi-actor applications** with LLMs. It uses graphs where:
- **Nodes** = Functions (retrieval, generation, etc.)
- **Edges** = Control flow (conditional routing)
- **State** = Shared data between nodes

### LangGraph in RAG Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    LangGraph State                       │
│  {query, context, retrieved_docs, response, history}   │
└─────────────────────────────────────────────────────────┘
                        ↕
┌─────────────────────────────────────────────────────────┐
│                    Graph Nodes                           │
│                                                          │
│  1. [Retrieve Node] → Query ChromaDB                    │
│  2. [Format Context Node] → Prepare prompt             │
│  3. [Generate Node] → Call LLM                          │
│  4. [Validate Node] → Check response quality            │
│  5. [Respond Node] → Return to user                     │
└─────────────────────────────────────────────────────────┘
```

### Benefits of Using LangGraph
- **Modular**: Each step is a separate node (easy to debug/modify)
- **Stateful**: Maintains conversation history
- **Conditional Logic**: Can route based on query type, confidence, etc.
- **Observable**: Easy to add logging, monitoring at each step
- **Extensible**: Add new nodes (e.g., fallback, human-in-the-loop)

---

## 🏗️ Architecture Overview

### High-Level Architecture

```
┌──────────────┐
│   User       │
│   Query      │
└──────┬───────┘
       │
       ▼
┌─────────────────────────────────────────────────┐
│           LangGraph Application                 │
│                                                 │
│  ┌──────────────┐      ┌──────────────┐       │
│  │  Retrieve    │─────▶│  Format      │       │
│  │  Node        │      │  Context     │       │
│  └──────────────┘      └──────┬───────┘       │
│                                │               │
│  ┌──────────────┐      ┌──────▼───────┐       │
│  │  Generate    │◀─────│  Generate    │       │
│  │  Response    │      │  Node       │       │
│  └──────────────┘      └──────────────┘       │
└─────────────────────────────────────────────────┘
       │                    │
       ▼                    ▼
┌──────────────┐    ┌──────────────┐
│  ChromaDB    │    │   Ollama     │
│  (Vector DB) │    │   (LLM)      │
└──────────────┘    └──────────────┘
```

### Data Flow

1. **User Input** → Chat interface receives query
2. **Retrieve Node** → 
   - Convert query to embedding (using existing `text_to_embeddings`)
   - Search ChromaDB (using existing `ChromaDBService.read()`)
   - Return top-k relevant documents
3. **Format Context Node** →
   - Combine retrieved documents
   - Build prompt template
   - Include conversation history (if multi-turn)
4. **Generate Node** →
   - Call Ollama LLM API (new: chat completion endpoint)
   - Pass formatted prompt
   - Get generated response
5. **Respond Node** →
   - Format response
   - Return to user
   - Update conversation history

---

## 📋 Implementation Plan

### Phase 1: Setup & Dependencies
- [ ] Install LangGraph and LangChain dependencies
- [ ] Set up Ollama chat model (not just embeddings)
- [ ] Create project structure
- [ ] Update `config.py` with LLM settings

### Phase 2: Core RAG Components
- [ ] Create `retrievers/` module with ChromaDB retriever
- [ ] Create `prompts/` module with prompt templates
- [ ] Create `llm/` module for Ollama chat integration
- [ ] Create utility functions for context formatting

### Phase 3: LangGraph Implementation
- [ ] Define LangGraph state schema
- [ ] Create graph nodes (retrieve, format, generate, respond)
- [ ] Define graph edges and conditional routing
- [ ] Build and compile the graph

### Phase 4: Chat Interface
- [ ] Create simple CLI chat interface
- [ ] Add conversation history management
- [ ] Implement streaming responses (optional)
- [ ] Add error handling

### Phase 5: Testing & Refinement
- [ ] Test with various queries
- [ ] Add response validation
- [ ] Implement fallback mechanisms
- [ ] Add logging and observability

---

## 📁 File Structure

```
embeddings-py/
├── config.py                          # ✅ Existing
├── db/
│   └── chromadb_service.py            # ✅ Existing
├── utils.py                           # ✅ Existing
├── mock-data/
│   └── payment_support_data.json      # ✅ Existing
│
├── rag/                               # 🆕 New RAG module
│   ├── __init__.py
│   ├── retriever.py                   # ChromaDB retriever wrapper
│   ├── prompts.py                     # Prompt templates
│   └── context_formatter.py           # Context formatting utilities
│
├── llm/                               # 🆕 LLM integration
│   ├── __init__.py
│   └── ollama_chat.py                 # Ollama chat completion client
│
├── langgraph_app/                     # 🆕 LangGraph application
│   ├── __init__.py
│   ├── state.py                       # State schema definition
│   ├── nodes.py                       # Graph nodes (functions)
│   ├── graph.py                       # Graph definition and compilation
│   └── chat.py                        # Chat interface
│
├── requirements.txt                   # Update with new dependencies
└── README_RAG.md                      # 🆕 RAG documentation
```

---

## 📦 Dependencies

### New Dependencies to Add

```txt
# Existing dependencies (keep these)
chromadb
requests
numpy

# New dependencies for RAG + LangGraph
langgraph>=0.2.0          # Core LangGraph framework
langchain>=0.3.0          # LangChain integration (used by LangGraph)
langchain-community>=0.3.0 # Community integrations
langchain-core>=0.3.0     # Core LangChain abstractions
```

### Optional (for better UX)
```txt
rich>=13.0.0              # Beautiful terminal output
typer>=0.9.0              # CLI framework (if building CLI)
```

---

## 🔨 Step-by-Step Implementation

### Step 1: Update Configuration (`config.py`)

Add LLM configuration:
```python
# Existing embedding config...
# Add:

# Ollama Chat Configuration
OLLAMA_CHAT_API_URL = "http://localhost:11434/api/chat"
CHAT_MODEL = "llama3.2"  # or "mistral", "qwen2", etc. (any chat model)
CHAT_TIMEOUT = 30  # seconds

# RAG Configuration
RETRIEVAL_TOP_K = 3  # Number of documents to retrieve
MAX_CONTEXT_LENGTH = 2000  # Max characters in context
ENABLE_CONVERSATION_HISTORY = True
MAX_HISTORY_LENGTH = 5  # Number of previous exchanges to keep
```

### Step 2: Create Retriever Module (`rag/retriever.py`)

**Purpose**: Wrap ChromaDB search in a clean interface for RAG

**Key Functions**:
- `retrieve_relevant_docs(query: str, top_k: int) -> List[Dict]`
  - Uses existing `ChromaDBService` and `text_to_embeddings`
  - Returns list of documents with metadata and similarity scores

**Implementation Notes**:
- Reuse `ChromaDBService.read(query_texts=[query], n_results=top_k)`
- Format results: `{text, metadata, score, id}`
- Filter by similarity threshold (optional)

### Step 3: Create LLM Chat Client (`llm/ollama_chat.py`)

**Purpose**: Interface with Ollama's chat completion API

**Key Functions**:
- `generate_response(messages: List[Dict]) -> str`
  - Send messages to Ollama chat API
  - Return generated text
  - Handle errors and timeouts

**Message Format**:
```python
messages = [
    {"role": "system", "content": "You are a helpful payment support assistant."},
    {"role": "user", "content": "What is my daily limit?"}
]
```

### Step 4: Create Prompt Templates (`rag/prompts.py`)

**Purpose**: Define how to format prompts for the LLM

**Key Templates**:
- `SYSTEM_PROMPT`: Instructions for the assistant
- `CONTEXT_PROMPT`: How to format retrieved context
- `USER_QUERY_PROMPT`: How to format user query

**Example Template**:
```python
SYSTEM_PROMPT = """You are a helpful payment support assistant. 
Answer questions based ONLY on the provided context. 
If the context doesn't contain the answer, say "I don't have that information."
"""

CONTEXT_FORMAT = """Context from knowledge base:
{context}
"""
```

### Step 5: Define LangGraph State (`langgraph_app/state.py`)

**Purpose**: Define the shared state structure

**State Schema**:
```python
from typing import TypedDict, List, Dict, Annotated
from langgraph.graph.message import add_messages

class GraphState(TypedDict):
    messages: Annotated[List[Dict], add_messages]  # Conversation history
    query: str                                      # Current user query
    retrieved_docs: List[Dict]                     # Retrieved documents
    context: str                                    # Formatted context
    response: str                                   # Generated response
    metadata: Dict                                  # Additional metadata
```

### Step 6: Create Graph Nodes (`langgraph_app/nodes.py`)

**Purpose**: Implement each step of the RAG pipeline

**Nodes**:

1. **`retrieve_node(state: GraphState) -> GraphState`**
   - Extract query from state
   - Call retriever to get relevant docs
   - Update `state["retrieved_docs"]`

2. **`format_context_node(state: GraphState) -> GraphState`**
   - Take retrieved docs
   - Format using prompt template
   - Update `state["context"]`

3. **`generate_node(state: GraphState) -> GraphState`**
   - Build messages: system + context + user query + history
   - Call LLM
   - Update `state["response"]`

4. **`respond_node(state: GraphState) -> GraphState`**
   - Format final response
   - Add to message history
   - Return state

### Step 7: Build the Graph (`langgraph_app/graph.py`)

**Purpose**: Connect nodes and define flow

**Graph Structure**:
```
START → retrieve_node → format_context_node → generate_node → respond_node → END
```

**Implementation**:
```python
from langgraph.graph import StateGraph

def create_graph():
    graph = StateGraph(GraphState)
    
    # Add nodes
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("format_context", format_context_node)
    graph.add_node("generate", generate_node)
    graph.add_node("respond", respond_node)
    
    # Define edges
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "format_context")
    graph.add_edge("format_context", "generate")
    graph.add_edge("generate", "respond")
    graph.set_finish_point("respond")
    
    return graph.compile()
```

### Step 8: Create Chat Interface (`langgraph_app/chat.py`)

**Purpose**: User-facing chat interface

**Features**:
- Simple CLI loop: `while True: query = input("You: ")`
- Initialize graph with empty state
- Invoke graph with user query
- Display response
- Handle exit commands (`/quit`, `/exit`)

**Example Flow**:
```python
graph = create_graph()

while True:
    query = input("\nYou: ").strip()
    if query.lower() in ["/quit", "/exit"]:
        break
    
    # Invoke graph
    result = graph.invoke({
        "messages": [],
        "query": query,
        "retrieved_docs": [],
        "context": "",
        "response": "",
        "metadata": {}
    })
    
    print(f"\nAssistant: {result['response']}")
```

### Step 9: Add Conversation History (Enhancement)

**Purpose**: Support multi-turn conversations

**Changes**:
- Update state initialization to preserve previous messages
- Modify `respond_node` to append to message history
- Update `generate_node` to include conversation history in prompt

### Step 10: Add Error Handling & Validation

**Purpose**: Make the app robust

**Add**:
- Try-catch in each node
- Validation node (check if retrieval found docs)
- Fallback node (if retrieval fails, use general response)
- Logging for debugging

---

## 🧪 Testing Strategy

### Unit Tests
- Test retriever with various queries
- Test prompt formatting
- Test LLM client with mock responses
- Test individual nodes in isolation

### Integration Tests
- Test full RAG pipeline end-to-end
- Test with different query types
- Test conversation history
- Test error scenarios

### Manual Testing Queries
1. **Direct match**: "What is my daily transaction limit?"
2. **Semantic match**: "How much can I spend per day?" (should retrieve limit info)
3. **Out of scope**: "What's the weather?" (should say it doesn't have that info)
4. **Multi-turn**: 
   - User: "Tell me about card blocking"
   - User: "How do I do that?" (should understand "that" = blocking)

---

## 🎓 Learning Objectives

By implementing this, you'll learn:

1. **RAG Fundamentals**:
   - How retrieval works with embeddings
   - How to augment prompts with context
   - How LLMs use context to generate answers

2. **LangGraph Concepts**:
   - State management in graph-based applications
   - Node-based architecture
   - Conditional routing and control flow

3. **Production Patterns**:
   - Modular code organization
   - Error handling in LLM applications
   - Conversation management
   - Prompt engineering

4. **Integration Skills**:
   - Connecting vector databases with LLMs
   - Building end-to-end AI applications
   - Debugging multi-step pipelines

---

## 🚀 Next Steps After Implementation

1. **Enhance Retrieval**:
   - Add re-ranking
   - Implement hybrid search (keyword + semantic)
   - Add metadata filtering

2. **Improve Generation**:
   - Add response streaming
   - Implement confidence scoring
   - Add citation of sources

3. **Add Features**:
   - Web interface (Streamlit/Gradio)
   - User feedback collection
   - Analytics and monitoring

4. **Optimize**:
   - Caching frequently asked questions
   - Batch processing
   - Performance tuning

---

## 📝 Notes

- Start simple: Get basic RAG working first, then add complexity
- Use existing code: Reuse `ChromaDBService` and `text_to_embeddings`
- Test incrementally: Test each node before building the full graph
- Document as you go: Add docstrings explaining RAG concepts
- Experiment: Try different prompt templates and retrieval strategies

---

## ✅ Checklist Before Starting Implementation

- [ ] Ollama is running with a chat model (not just embedding model)
- [ ] ChromaDB has embeddings stored (run `payment_support_embeddings.py`)
- [ ] Python 3.8+ is installed
- [ ] Virtual environment is set up (recommended)
- [ ] You understand the existing codebase structure

---

**Ready to build? Start with Phase 1 and work through each step methodically!** 🎯

---

## 🔄 Complete Flow Diagram: Final Product

### End-to-End System Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACE (CLI)                               │
│                                                                              │
│   User types: "What is my daily transaction limit?"                         │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LANGGRAPH APPLICATION (Main Entry)                        │
│                                                                              │
│   chat.py: main()                                                           │
│   ├─ Initialize GraphState                                                  │
│   └─ graph.invoke(initial_state)                                           │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LANGGRAPH STATE INITIALIZATION                      │
│                                                                              │
│   GraphState = {                                                            │
│     "messages": [],                    # Empty conversation history        │
│     "query": "What is my daily...",     # User query                       │
│     "retrieved_docs": [],              # Will be populated                │
│     "context": "",                     # Will be formatted                │
│     "response": "",                    # Will be generated                │
│     "metadata": {}                      # Additional info                  │
│   }                                                                         │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         NODE 1: RETRIEVE NODE                                │
│                    (langgraph_app/nodes.py: retrieve_node)                  │
│                                                                              │
│   Input State:                                                               │
│     - query: "What is my daily transaction limit?"                         │
│                                                                              │
│   Process:                                                                   │
│   1. Extract query from state                                              │
│   2. Call rag/retriever.py: retrieve_relevant_docs()                      │
│      │                                                                      │
│      ├─→ utils.py: text_to_embeddings([query])                             │
│      │   │                                                                  │
│      │   └─→ Ollama API: POST /api/embed                                    │
│      │       │                                                               │
│      │       └─→ Returns: [0.123, -0.456, ..., 0.789] (embedding vector)   │
│      │                                                                      │
│      └─→ db/chromadb_service.py: read(query_texts=[query], n_results=3)    │
│          │                                                                  │
│          └─→ ChromaDB: Vector Similarity Search                            │
│              │                                                               │
│              └─→ Returns: Top 3 similar documents with scores                │
│                                                                              │
│   Output State:                                                              │
│     - retrieved_docs: [                                                     │
│         {                                                                   │
│           "text": "Your daily transaction limit...",                       │
│           "metadata": {"category": "transaction_limits"},                   │
│           "score": 0.85,                                                   │
│           "id": "support_001"                                              │
│         },                                                                 │
│         ... (2 more docs)                                                  │
│       ]                                                                     │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    NODE 2: FORMAT CONTEXT NODE                               │
│              (langgraph_app/nodes.py: format_context_node)                  │
│                                                                              │
│   Input State:                                                               │
│     - retrieved_docs: [3 documents with text, metadata, scores]            │
│                                                                              │
│   Process:                                                                   │
│   1. Extract retrieved_docs from state                                     │
│   2. Call rag/context_formatter.py: format_context()                       │
│      │                                                                      │
│      ├─→ rag/prompts.py: CONTEXT_FORMAT template                           │
│      │                                                                      │
│      └─→ Combine documents:                                                │
│          """                                                                │
│          Context from knowledge base:                                       │
│                                                                             │
│          [1] Category: transaction_limits                                   │
│          Your daily transaction limit depends on your account tier...      │
│                                                                             │
│          [2] Category: transaction_limits                                   │
│          ... (more context)                                                │
│          """                                                                │
│                                                                              │
│   Output State:                                                              │
│     - context: "Context from knowledge base:\n[1] Category: ..."           │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        NODE 3: GENERATE NODE                                  │
│                 (langgraph_app/nodes.py: generate_node)                     │
│                                                                              │
│   Input State:                                                               │
│     - query: "What is my daily transaction limit?"                         │
│     - context: "Context from knowledge base: ..."                           │
│     - messages: [] (or previous conversation history)                       │
│                                                                              │
│   Process:                                                                   │
│   1. Build messages array:                                                  │
│      [                                                                      │
│        {                                                                    │
│          "role": "system",                                                  │
│          "content": "You are a helpful payment support assistant..."        │
│        },                                                                   │
│        {                                                                    │
│          "role": "user",                                                    │
│          "content": "Context: ...\n\nQuestion: What is my daily limit?"     │
│        }                                                                    │
│      ]                                                                      │
│                                                                              │
│   2. Call llm/ollama_chat.py: generate_response(messages)                  │
│      │                                                                      │
│      └─→ Ollama API: POST /api/chat                                         │
│          │                                                                  │
│          │ Request:                                                         │
│          │ {                                                                │
│          │   "model": "llama3.2",                                          │
│          │   "messages": [                                                  │
│          │     {"role": "system", "content": "..."},                       │
│          │     {"role": "user", "content": "..."}                          │
│          │   ]                                                              │
│          │ }                                                                │
│          │                                                                  │
│          └─→ Response:                                                     │
│              {                                                              │
│                "message": {                                                 │
│                  "content": "Your daily transaction limit depends on..."   │
│                }                                                            │
│              }                                                              │
│                                                                              │
│   Output State:                                                              │
│     - response: "Your daily transaction limit depends on your account..."  │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         NODE 4: RESPOND NODE                                 │
│                  (langgraph_app/nodes.py: respond_node)                     │
│                                                                              │
│   Input State:                                                               │
│     - response: "Your daily transaction limit depends on..."               │
│     - query: "What is my daily transaction limit?"                         │
│     - messages: [] (previous history)                                      │
│                                                                              │
│   Process:                                                                   │
│   1. Format final response                                                 │
│   2. Update conversation history:                                          │
│      messages.append({"role": "user", "content": query})                   │
│      messages.append({"role": "assistant", "content": response})          │
│   3. Prepare final state                                                    │
│                                                                              │
│   Output State:                                                              │
│     - response: "Your daily transaction limit depends on..."                │
│     - messages: [                                                          │
│         {"role": "user", "content": "What is my daily..."},                │
│         {"role": "assistant", "content": "Your daily..."}                  │
│       ]                                                                     │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LANGGRAPH COMPLETION                                 │
│                                                                              │
│   Graph execution complete                                                  │
│   Final state returned to chat.py                                           │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CHAT INTERFACE OUTPUT                               │
│                                                                              │
│   chat.py extracts response from state                                      │
│   Prints: "Assistant: Your daily transaction limit depends on..."          │
│                                                                              │
│   ┌────────────────────────────────────────────────────────┐               │
│   │ You: What is my daily transaction limit?              │               │
│   │                                                        │               │
│   │ Assistant: Your daily transaction limit depends on    │               │
│   │            your account tier. Basic accounts have a    │               │
│   │            limit of £1,000 per day, Premium accounts   │               │
│   │            have £5,000 per day, and Metal accounts     │               │
│   │            have £10,000 per day.                      │               │
│   └────────────────────────────────────────────────────────┘               │
│                                                                              │
│   Loop continues: Waiting for next user input...                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Component Interaction Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          COMPLETE SYSTEM ARCHITECTURE                        │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐
│    USER      │
└──────┬───────┘
       │
       │ 1. User Query
       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LANGGRAPH APPLICATION                                │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                         GRAPH EXECUTION                               │  │
│  │                                                                       │  │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │  │
│  │  │   RETRIEVE   │───▶│   FORMAT     │───▶│   GENERATE   │          │  │
│  │  │    NODE      │    │   CONTEXT    │    │    NODE      │          │  │
│  │  └──────┬───────┘    └──────────────┘    └──────┬───────┘          │  │
│  │         │                                        │                   │  │
│  │         │                                        │                   │  │
│  │         ▼                                        ▼                   │  │
│  │  ┌──────────────┐                        ┌──────────────┐          │  │
│  │  │   RESPOND    │                        │   STATE      │          │  │
│  │  │    NODE      │                        │   MANAGER    │          │  │
│  │  └──────────────┘                        └──────────────┘          │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└───────┬───────────────────────────────────────────────────────────┬─────────┘
        │                                                           │
        │ 2. Query Embedding                                       │ 5. Chat Request
        │    (text_to_embeddings)                                  │    (generate_response)
        │                                                           │
        ▼                                                           ▼
┌──────────────┐                                            ┌──────────────┐
│   CHROMADB   │                                            │    OLLAMA    │
│              │                                            │              │
│  ┌────────┐ │                                            │  ┌────────┐  │
│  │ Vector │ │                                            │  │  LLM   │  │
│  │  Store │ │                                            │  │  Chat  │  │
│  │        │ │                                            │  │  Model │  │
│  └────────┘ │                                            │  └────────┘  │
│              │                                            │              │
│  3. Semantic│                                            │  6. Response│
│     Search  │                                            │     Text     │
│             │                                            │              │
│  4. Top-K   │                                            │              │
│     Docs    │                                            │              │
└──────────────┘                                            └──────────────┘
        │                                                           │
        │                                                           │
        └───────────────────────────────────────────────────────────┘
                              │
                              │ 7. Final Response
                              ▼
                       ┌──────────────┐
                       │     USER     │
                       └──────────────┘
```

### Data Flow Sequence

```
┌─────────┐  ┌──────────────┐  ┌──────────┐  ┌──────────────┐  ┌──────────┐
│  User   │  │  LangGraph   │  │ ChromaDB │  │   Ollama     │  │  User    │
│         │  │              │  │          │  │              │  │          │
│         │  │              │  │          │  │              │  │          │
│ Query   │─▶│ Retrieve     │─▶│ Search   │  │              │  │          │
│         │  │              │◀─│ Results  │  │              │  │          │
│         │  │              │  │          │  │              │  │          │
│         │  │ Format       │  │          │  │              │  │          │
│         │  │ Context      │  │          │  │              │  │          │
│         │  │              │  │          │  │              │  │          │
│         │  │ Generate     │  │          │─▶│ Chat API     │  │          │
│         │  │              │  │          │  │              │  │          │
│         │  │              │  │          │◀─│ Response     │  │          │
│         │  │              │  │          │  │              │  │          │
│         │  │ Respond      │  │          │  │              │  │          │
│         │◀─│              │  │          │  │              │  │          │
│ Answer  │  │              │  │          │  │              │  │          │
└─────────┘  └──────────────┘  └──────────┘  └──────────────┘  └──────────┘
```

### State Evolution Through Nodes

```
Initial State:
┌─────────────────────────────────────────────────────────────┐
│ {                                                            │
│   "messages": [],                                           │
│   "query": "What is my daily transaction limit?",          │
│   "retrieved_docs": [],                                     │
│   "context": "",                                            │
│   "response": "",                                           │
│   "metadata": {}                                            │
│ }                                                            │
└─────────────────────────────────────────────────────────────┘
                    │
                    ▼
After RETRIEVE Node:
┌─────────────────────────────────────────────────────────────┐
│ {                                                            │
│   "messages": [],                                           │
│   "query": "What is my daily transaction limit?",          │
│   "retrieved_docs": [                                       │
│     {"text": "...", "metadata": {...}, "score": 0.85},    │
│     ...                                                     │
│   ],                                                        │
│   "context": "",                                            │
│   "response": "",                                           │
│   "metadata": {}                                            │
│ }                                                            │
└─────────────────────────────────────────────────────────────┘
                    │
                    ▼
After FORMAT_CONTEXT Node:
┌─────────────────────────────────────────────────────────────┐
│ {                                                            │
│   "messages": [],                                           │
│   "query": "What is my daily transaction limit?",          │
│   "retrieved_docs": [...],                                  │
│   "context": "Context from knowledge base:\n[1] Category...",│
│   "response": "",                                           │
│   "metadata": {}                                            │
│ }                                                            │
└─────────────────────────────────────────────────────────────┘
                    │
                    ▼
After GENERATE Node:
┌─────────────────────────────────────────────────────────────┐
│ {                                                            │
│   "messages": [],                                           │
│   "query": "What is my daily transaction limit?",          │
│   "retrieved_docs": [...],                                  │
│   "context": "...",                                         │
│   "response": "Your daily transaction limit depends on...", │
│   "metadata": {}                                            │
│ }                                                            │
└─────────────────────────────────────────────────────────────┘
                    │
                    ▼
After RESPOND Node (Final State):
┌─────────────────────────────────────────────────────────────┐
│ {                                                            │
│   "messages": [                                            │
│     {"role": "user", "content": "What is my daily..."},   │
│     {"role": "assistant", "content": "Your daily..."}      │
│   ],                                                        │
│   "query": "What is my daily transaction limit?",          │
│   "retrieved_docs": [...],                                  │
│   "context": "...",                                         │
│   "response": "Your daily transaction limit depends on...", │
│   "metadata": {"retrieval_count": 3, "model": "llama3.2"}  │
│ }                                                            │
└─────────────────────────────────────────────────────────────┘
```

### Multi-Turn Conversation Flow

```
Turn 1:
User: "What is my daily transaction limit?"
  → Retrieve → Format → Generate → Respond
  → Response: "Your daily limit depends on your account tier..."

Turn 2:
User: "How do I check it?"
  → State includes previous messages
  → Retrieve (may find related docs about checking limits)
  → Format (includes conversation context)
  → Generate (LLM understands "it" = transaction limit)
  → Respond: "You can check your current limit in the app..."

Turn 3:
User: "What about card blocking?"
  → New topic, retrieves card management docs
  → Format → Generate → Respond
  → Response: "To block your card, go to the Cards section..."
```

---

**This diagram shows the complete end-to-end flow of the RAG + LangGraph chat support application!** 🎯

