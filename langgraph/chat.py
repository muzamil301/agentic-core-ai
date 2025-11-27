"""
Chat Interface - CLI for interacting with the RAG service.

This module provides a simple command-line interface for chatting
with the RAG-powered support assistant.
"""

from langgraph.service.rag_service import RAGService


def main():
    """
    Main chat interface loop.
    
    Provides an interactive CLI for chatting with the RAG service.
    """
    print("=" * 70)
    print("🤖 Payment Support Assistant (RAG + LangGraph)")
    print("=" * 70)
    print("\nType your questions below. Type '/quit' or '/exit' to exit.")
    print("Type '/reset' to reset conversation history.")
    print("Type '/history' to view conversation history.")
    print("-" * 70)
    
    # Initialize RAG service
    try:
        service = RAGService()
        print("\n✅ RAG service initialized successfully!")
    except Exception as e:
        print(f"\n❌ Failed to initialize RAG service: {e}")
        print("Please ensure:")
        print("  1. Ollama is running with a chat model")
        print("  2. ChromaDB has embeddings stored")
        print("  3. All dependencies are installed")
        return
    
    # Chat loop
    while True:
        try:
            # Get user input
            query = input("\n💬 You: ").strip()
            
            # Handle commands
            if query.lower() in ["/quit", "/exit", "/q"]:
                print("\n👋 Goodbye!")
                break
            
            if query.lower() == "/reset":
                service.reset_conversation()
                print("\n🔄 Conversation history reset.")
                continue
            
            if query.lower() == "/history":
                history = service.get_conversation_history()
                if history:
                    print("\n📜 Conversation History:")
                    print("-" * 70)
                    for msg in history:
                        role = msg.get("role", "unknown")
                        content = msg.get("content", "")
                        role_icon = "👤" if role == "user" else "🤖"
                        print(f"{role_icon} {role.capitalize()}: {content[:100]}{'...' if len(content) > 100 else ''}")
                else:
                    print("\n📜 No conversation history yet.")
                continue
            
            if not query:
                continue
            
            # Process query
            print("\n🤔 Thinking...")
            result = service.chat(query)
            
            # Display response
            response = result.get("response", "I'm sorry, I couldn't generate a response.")
            print(f"\n🤖 Assistant: {response}")
            
            # Show metadata if there are retrieved docs
            retrieved_docs = result.get("retrieved_docs", [])
            if retrieved_docs:
                print(f"\n📚 Retrieved {len(retrieved_docs)} relevant document(s)")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again or type '/quit' to exit.")


if __name__ == "__main__":
    main()




