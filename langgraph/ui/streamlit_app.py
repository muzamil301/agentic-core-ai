"""
Streamlit Web UI for RAG Chat Application

A modern web interface for chatting with the RAG-powered support assistant.
"""

import streamlit as st
import sys
from pathlib import Path
from typing import Dict, Any
import time

# Add parent directory to path
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from langgraph.service.rag_service import RAGService

# Page configuration
st.set_page_config(
    page_title="Payment Support Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    .user-message {
        background-color: #f0f2f6;
        border-left-color: #667eea;
    }
    
    .assistant-message {
        background-color: #e8f4fd;
        border-left-color: #1f77b4;
    }
    
    .system-message {
        background-color: #fff3cd;
        border-left-color: #ffc107;
        font-size: 0.9em;
    }
    
    .metrics-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "rag_service" not in st.session_state:
        try:
            st.session_state.rag_service = RAGService()
            st.session_state.service_initialized = True
        except Exception as e:
            st.session_state.service_initialized = False
            st.session_state.service_error = str(e)
    
    if "conversation_count" not in st.session_state:
        st.session_state.conversation_count = 0

def display_header():
    """Display the main header."""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Payment Support Assistant</h1>
        <p>Powered by RAG + LangGraph | Ask questions about payments, cards, and transfers</p>
    </div>
    """, unsafe_allow_html=True)

def display_sidebar():
    """Display the sidebar with controls and information."""
    with st.sidebar:
        st.header("🔧 Controls")
        
        # Reset conversation button
        if st.button("🔄 Reset Conversation", use_container_width=True):
            st.session_state.messages = []
            if st.session_state.service_initialized:
                st.session_state.rag_service.reset_conversation()
            st.session_state.conversation_count = 0
            st.rerun()
        
        # Service status
        st.header("📊 Service Status")
        if st.session_state.service_initialized:
            st.success("✅ RAG Service: Online")
        else:
            st.error("❌ RAG Service: Offline")
            if hasattr(st.session_state, 'service_error'):
                st.error(f"Error: {st.session_state.service_error}")
        
        # Conversation metrics
        st.header("📈 Metrics")
        st.metric("Conversation Turns", st.session_state.conversation_count)
        st.metric("Total Messages", len(st.session_state.messages))
        
        # Example queries
        st.header("💡 Example Queries")
        example_queries = [
            "What is my daily transaction limit?",
            "How do I block my card?",
            "How long do international transfers take?",
            "What are the different account tiers?",
            "How do I unfreeze my card?",
        ]
        
        for query in example_queries:
            if st.button(f"💬 {query[:30]}...", key=f"example_{query}", use_container_width=True):
                st.session_state.example_query = query
                st.rerun()

def display_chat_message(role: str, content: str, metadata: Dict[str, Any] = None):
    """Display a chat message with proper styling."""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 You:</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
    
    elif role == "assistant":
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>🤖 Assistant:</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
        
        # Show metadata if available
        if metadata:
            with st.expander("📋 Response Details", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    if "retrieval_count" in metadata:
                        st.metric("Documents Retrieved", metadata["retrieval_count"])
                    if "generation_success" in metadata:
                        st.success("✅ Generation Successful" if metadata["generation_success"] else "❌ Generation Failed")
                
                with col2:
                    if "query_type" in metadata:
                        st.info(f"Query Type: {metadata['query_type']}")
                    if "response_time" in metadata:
                        st.metric("Response Time", f"{metadata['response_time']:.2f}s")
    
    elif role == "system":
        st.markdown(f"""
        <div class="chat-message system-message">
            <strong>ℹ️ System:</strong> {content}
        </div>
        """, unsafe_allow_html=True)

def process_query(query: str) -> Dict[str, Any]:
    """Process a user query and return the response."""
    if not st.session_state.service_initialized:
        return {
            "response": "Sorry, the RAG service is not available. Please check the service status in the sidebar.",
            "metadata": {"error": "Service not initialized"}
        }
    
    try:
        start_time = time.time()
        result = st.session_state.rag_service.chat(query)
        end_time = time.time()
        
        # Add response time to metadata
        result["metadata"]["response_time"] = end_time - start_time
        
        return result
    
    except Exception as e:
        return {
            "response": f"I encountered an error while processing your query: {str(e)}",
            "metadata": {"error": str(e)}
        }

def main():
    """Main application function."""
    initialize_session_state()
    display_header()
    display_sidebar()
    
    # Check for example query from sidebar
    if hasattr(st.session_state, 'example_query'):
        query = st.session_state.example_query
        delattr(st.session_state, 'example_query')
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": query})
        
        # Process query
        with st.spinner("🤔 Thinking..."):
            result = process_query(query)
        
        # Add assistant response
        st.session_state.messages.append({
            "role": "assistant", 
            "content": result["response"],
            "metadata": result.get("metadata", {})
        })
        
        st.session_state.conversation_count += 1
        st.rerun()
    
    # Display chat history
    st.header("💬 Conversation")
    
    if not st.session_state.messages:
        st.info("👋 Welcome! Ask me anything about payments, cards, or transfers. Try one of the example queries from the sidebar!")
    
    for message in st.session_state.messages:
        display_chat_message(
            message["role"], 
            message["content"], 
            message.get("metadata")
        )
    
    # Chat input
    st.header("✍️ Ask a Question")
    
    # Create columns for input and button
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Type your question here...",
            placeholder="e.g., What is my daily transaction limit?",
            key="user_input",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Send 📤", use_container_width=True)
    
    # Process input
    if send_button and user_input.strip():
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Process query
        with st.spinner("🤔 Thinking..."):
            result = process_query(user_input)
        
        # Add assistant response
        st.session_state.messages.append({
            "role": "assistant", 
            "content": result["response"],
            "metadata": result.get("metadata", {})
        })
        
        st.session_state.conversation_count += 1
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9em;">
        Built with ❤️ using Streamlit, LangGraph, and ChromaDB<br>
        <em>This is a demo application for learning purposes</em>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

