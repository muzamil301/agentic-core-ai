"""
Ollama Chat Client for LangGraph RAG Service

This module provides functionality to interact with Ollama's chat API
for generating LLM responses.
"""

import requests
from typing import List, Dict, Any, Optional
from langgraph_service.config import (
    OLLAMA_CHAT_API_URL,
    CHAT_MODEL,
    OLLAMA_TIMEOUT,
)


class OllamaChatClient:
    """
    Client for interacting with Ollama's chat completion API.
    
    This class:
    1. Sends chat messages to Ollama
    2. Receives LLM-generated responses
    3. Handles errors gracefully
    4. Supports conversation history
    """
    
    def __init__(
        self,
        model: str = CHAT_MODEL,
        api_url: str = OLLAMA_CHAT_API_URL,
        timeout: int = OLLAMA_TIMEOUT,
    ):
        """
        Initialize the Ollama chat client.
        
        Args:
            model: Name of the chat model (default from config)
            api_url: Ollama chat API URL (default from config)
            timeout: Request timeout in seconds (default from config)
        """
        self.model = model
        self.api_url = api_url
        self.timeout = timeout
    
    def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        stream: bool = False,
    ) -> str:
        """
        Generate a response from Ollama based on chat messages.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
                     Example: [
                         {"role": "user", "content": "Hello"},
                         {"role": "assistant", "content": "Hi there!"},
                         {"role": "user", "content": "How are you?"}
                     ]
            system_prompt: Optional system prompt to guide the model behavior
            stream: Whether to stream the response (not implemented yet)
            
        Returns:
            Generated response string from the LLM
            
        Raises:
            ValueError: If messages are invalid
            ConnectionError: If Ollama API is unavailable
        """
        if not messages:
            raise ValueError("Messages list cannot be empty")
        
        # Validate message format
        for msg in messages:
            if not isinstance(msg, dict):
                raise ValueError("Each message must be a dictionary")
            if "role" not in msg or "content" not in msg:
                raise ValueError("Each message must have 'role' and 'content' keys")
            if msg["role"] not in ["system", "user", "assistant"]:
                raise ValueError(f"Invalid role: {msg['role']}. Must be 'system', 'user', or 'assistant'")
        
        # Prepare messages for API
        api_messages = messages.copy()
        
        # Add system prompt if provided
        if system_prompt:
            # Check if first message is already a system message
            if api_messages and api_messages[0].get("role") == "system":
                # Update existing system message
                api_messages[0]["content"] = system_prompt
            else:
                # Prepend system message
                api_messages.insert(0, {
                    "role": "system",
                    "content": system_prompt
                })
        
        # Prepare request payload
        payload = {
            "model": self.model,
            "messages": api_messages,
            "stream": stream,
        }
        
        try:
            # Make API request
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            # Parse response
            result = response.json()
            
            # Extract message content
            message = result.get("message", {})
            content = message.get("content", "")
            
            if not content:
                raise ConnectionError("Empty response from Ollama API")
            
            return content.strip()
            
        except requests.exceptions.Timeout:
            raise ConnectionError(
                f"Request to Ollama API timed out after {self.timeout} seconds. "
                f"Please ensure Ollama is running and the model '{self.model}' is available."
            )
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Failed to connect to Ollama API at {self.api_url}. "
                f"Please ensure Ollama is running: ollama serve"
            )
        except requests.exceptions.HTTPError as e:
            raise ConnectionError(
                f"Ollama API returned an error: {e}. "
                f"Status code: {response.status_code if 'response' in locals() else 'unknown'}"
            )
        except requests.exceptions.RequestException as e:
            raise ConnectionError(
                f"Failed to generate response from Ollama: {e}. "
                f"Please check your Ollama installation and API endpoint."
            )
        except KeyError as e:
            raise ConnectionError(
                f"Unexpected response format from Ollama API: missing key {e}"
            )
        except Exception as e:
            raise ConnectionError(
                f"Unexpected error while generating response: {e}"
            )
    
    def chat(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        system_prompt: Optional[str] = None,
    ) -> str:
        """
        Convenience method for simple chat interactions.
        
        Args:
            user_message: The user's message
            conversation_history: Optional list of previous messages
            system_prompt: Optional system prompt
            
        Returns:
            Generated response string
        """
        messages = []
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Generate response
        response = self.generate_response(
            messages=messages,
            system_prompt=system_prompt
        )
        
        return response


def generate_response(
    messages: List[Dict[str, str]],
    system_prompt: Optional[str] = None,
    model: str = CHAT_MODEL,
) -> str:
    """
    Convenience function to generate a response from Ollama.
    
    Args:
        messages: List of message dictionaries
        system_prompt: Optional system prompt
        model: Model name (default from config)
        
    Returns:
        Generated response string
    """
    client = OllamaChatClient(model=model)
    return client.generate_response(messages=messages, system_prompt=system_prompt)

