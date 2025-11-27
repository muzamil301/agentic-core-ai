"""
Ollama Chat Client for LLM interactions.

This module provides an interface for interacting with Ollama's chat API.
"""

import requests
from typing import List, Dict, Any, Optional
from langgraph.config.settings import (
    OLLAMA_CHAT_API_URL,
    CHAT_MODEL,
    CHAT_TIMEOUT,
)


class OllamaChatClient:
    """
    Client for interacting with Ollama's chat completion API.
    """
    
    def __init__(
        self,
        model: str = CHAT_MODEL,
        api_url: str = OLLAMA_CHAT_API_URL,
        timeout: int = CHAT_TIMEOUT
    ):
        """
        Initialize the Ollama chat client.
        
        Args:
            model: Name of the chat model to use
            api_url: Ollama chat API URL
            timeout: Request timeout in seconds
        """
        self.model = model
        self.api_url = api_url
        self.timeout = timeout
    
    def generate_response(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False
    ) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys.
                     Roles can be: 'system', 'user', 'assistant'
            stream: Whether to stream the response (not implemented yet)
        
        Returns:
            Generated response text
        
        Raises:
            ConnectionError: If API call fails
        """
        if not messages:
            raise ValueError("Messages list cannot be empty")
        
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream
        }
        
        try:
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Extract message content from response
            message = result.get("message", {})
            content = message.get("content", "")
            
            if not content:
                raise ValueError("Empty response from Ollama API")
            
            return content.strip()
            
        except requests.exceptions.RequestException as e:
            raise ConnectionError(
                f"Failed to generate response from Ollama: {e}. "
                f"Please ensure Ollama is running and the model '{self.model}' is available."
            )
    
    def chat(
        self,
        user_message: str,
        system_message: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Convenience method for simple chat interactions.
        
        Args:
            user_message: User's message
            system_message: Optional system message
            conversation_history: Optional conversation history
        
        Returns:
            Generated response
        """
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        if conversation_history:
            messages.extend(conversation_history)
        
        messages.append({"role": "user", "content": user_message})
        
        return self.generate_response(messages)




