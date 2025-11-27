import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, RotateCcw, Loader2 } from 'lucide-react';
import ChatMessage from './components/ChatMessage';
import { chatService } from './services/chatService';
import './styles/App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const messagesEndRef = useRef(null);

  // Scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Check connection status on mount
  useEffect(() => {
    checkConnection();
  }, []);

  const checkConnection = async () => {
    try {
      const status = await chatService.getStatus();
      setIsConnected(status.connected);
    } catch (error) {
      setIsConnected(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: inputValue.trim(),
      sender: 'user',
      timestamp: new Date()
    };

    // Add user message immediately
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await chatService.sendMessage(userMessage.text);
      
      const assistantMessage = {
        id: Date.now() + 1,
        text: response.response,
        sender: 'assistant',
        timestamp: new Date(),
        metadata: response.metadata
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: `Sorry, I encountered an error: ${error.message}`,
        sender: 'assistant',
        timestamp: new Date(),
        isError: true
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setMessages([]);
    chatService.resetConversation();
  };

  const exampleQueries = [
    "What is my daily transaction limit?",
    "How do I block my card?",
    "How long do international transfers take?",
    "Hello, how are you?",
    "Tell me about account tiers"
  ];

  const handleExampleClick = (query) => {
    setInputValue(query);
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <div className="header-title">
            <Bot className="header-icon" />
            <h1>Payment Support Assistant</h1>
          </div>
          <div className="header-status">
            <div className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
              <div className="status-dot"></div>
              <span>{isConnected ? 'Connected' : 'Disconnected'}</span>
            </div>
            <button 
              className="reset-button"
              onClick={handleReset}
              title="Reset Conversation"
            >
              <RotateCcw size={18} />
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="app-content">
        {/* Sidebar with Examples */}
        <aside className="sidebar">
          <div className="sidebar-content">
            <h3>💡 Example Queries</h3>
            <div className="example-queries">
              {exampleQueries.map((query, index) => (
                <button
                  key={index}
                  className="example-button"
                  onClick={() => handleExampleClick(query)}
                >
                  {query}
                </button>
              ))}
            </div>
            
            <div className="sidebar-info">
              <h4>🤖 How it works</h4>
              <ul>
                <li>Ask payment-related questions for detailed answers</li>
                <li>General questions get direct responses</li>
                <li>Conversation history is maintained</li>
                <li>Smart routing between RAG and direct answers</li>
              </ul>
            </div>
          </div>
        </aside>

        {/* Chat Area */}
        <main className="chat-container">
          <div className="messages-container">
            {messages.length === 0 ? (
              <div className="welcome-message">
                <Bot size={48} className="welcome-icon" />
                <h2>Welcome to Payment Support!</h2>
                <p>Ask me anything about payments, cards, transfers, or account management.</p>
                <p>Try one of the example queries from the sidebar to get started.</p>
              </div>
            ) : (
              messages.map((message) => (
                <ChatMessage key={message.id} message={message} />
              ))
            )}
            
            {isLoading && (
              <div className="loading-message">
                <div className="message-avatar assistant">
                  <Loader2 className="loading-spinner" />
                </div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Input Form */}
          <form className="input-form" onSubmit={handleSendMessage}>
            <div className="input-container">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Type your message here..."
                className="message-input"
                disabled={isLoading || !isConnected}
              />
              <button
                type="submit"
                className="send-button"
                disabled={!inputValue.trim() || isLoading || !isConnected}
              >
                <Send size={20} />
              </button>
            </div>
          </form>
        </main>
      </div>
    </div>
  );
}

export default App;
