import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ChatService {
  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000, // 30 seconds timeout
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor for logging
    this.api.interceptors.request.use(
      (config) => {
        console.log('API Request:', config.method?.toUpperCase(), config.url);
        return config;
      },
      (error) => {
        console.error('API Request Error:', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor for error handling
    this.api.interceptors.response.use(
      (response) => {
        console.log('API Response:', response.status, response.data);
        return response;
      },
      (error) => {
        console.error('API Response Error:', error);
        
        if (error.code === 'ECONNABORTED') {
          throw new Error('Request timeout - please try again');
        }
        
        if (error.response) {
          // Server responded with error status
          const message = error.response.data?.detail || error.response.data?.message || 'Server error';
          throw new Error(message);
        } else if (error.request) {
          // Request made but no response received
          throw new Error('Unable to connect to server. Please check if the backend is running.');
        } else {
          // Something else happened
          throw new Error(error.message || 'An unexpected error occurred');
        }
      }
    );
  }

  async sendMessage(message) {
    try {
      const response = await this.api.post('/chat', {
        message: message,
        reset_history: false
      });
      
      return response.data;
    } catch (error) {
      console.error('Send message error:', error);
      throw error;
    }
  }

  async resetConversation() {
    try {
      const response = await this.api.post('/chat/reset');
      return response.data;
    } catch (error) {
      console.error('Reset conversation error:', error);
      throw error;
    }
  }

  async getStatus() {
    try {
      const response = await this.api.get('/status');
      return response.data;
    } catch (error) {
      console.error('Get status error:', error);
      throw error;
    }
  }

  async getConversationHistory() {
    try {
      const response = await this.api.get('/chat/history');
      return response.data;
    } catch (error) {
      console.error('Get history error:', error);
      throw error;
    }
  }
}

export const chatService = new ChatService();
