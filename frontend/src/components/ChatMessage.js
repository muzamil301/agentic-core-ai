import React, { useState } from 'react';
import { User, Bot, ChevronDown, ChevronUp } from 'lucide-react';

const ChatMessage = ({ message }) => {
  const [showMetadata, setShowMetadata] = useState(false);
  
  const isUser = message.sender === 'user';
  const hasMetadata = message.metadata && Object.keys(message.metadata).length > 0;

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const getQueryTypeColor = (queryType) => {
    switch (queryType) {
      case 'rag_required': return '#4CAF50';
      case 'direct_answer': return '#2196F3';
      case 'greeting': return '#FF9800';
      default: return '#757575';
    }
  };

  return (
    <div className={`message ${isUser ? 'user' : 'assistant'} ${message.isError ? 'error' : ''}`}>
      <div className="message-avatar">
        {isUser ? <User size={20} /> : <Bot size={20} />}
      </div>
      
      <div className="message-content">
        <div className="message-text">
          {message.text}
        </div>
        
        <div className="message-footer">
          <span className="message-time">
            {formatTime(message.timestamp)}
          </span>
          
          {hasMetadata && (
            <button
              className="metadata-toggle"
              onClick={() => setShowMetadata(!showMetadata)}
            >
              Details {showMetadata ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
            </button>
          )}
        </div>

        {showMetadata && hasMetadata && (
          <div className="message-metadata">
            <div className="metadata-grid">
              {message.metadata.query_type && (
                <div className="metadata-item">
                  <span className="metadata-label">Query Type:</span>
                  <span 
                    className="metadata-value query-type"
                    style={{ color: getQueryTypeColor(message.metadata.query_type) }}
                  >
                    {message.metadata.query_type.replace('_', ' ')}
                  </span>
                </div>
              )}
              
              {message.metadata.classification_confidence && (
                <div className="metadata-item">
                  <span className="metadata-label">Confidence:</span>
                  <span className="metadata-value">
                    {(message.metadata.classification_confidence * 100).toFixed(1)}%
                  </span>
                </div>
              )}
              
              {message.metadata.retrieval_count !== undefined && (
                <div className="metadata-item">
                  <span className="metadata-label">Documents Retrieved:</span>
                  <span className="metadata-value">
                    {message.metadata.retrieval_count}
                  </span>
                </div>
              )}
              
              {message.metadata.response_type && (
                <div className="metadata-item">
                  <span className="metadata-label">Response Type:</span>
                  <span className="metadata-value">
                    {message.metadata.response_type}
                  </span>
                </div>
              )}
              
              {message.metadata.response_time && (
                <div className="metadata-item">
                  <span className="metadata-label">Response Time:</span>
                  <span className="metadata-value">
                    {message.metadata.response_time.toFixed(2)}s
                  </span>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;
