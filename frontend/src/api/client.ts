import axios from 'axios';
import type { ChatRequest, ChatHistoryResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface StreamCallback {
  onToken: (token: string) => void;
  onComplete: () => void;
  onError: (error: Error) => void;
}

export const sendChatMessage = async (
  request: ChatRequest,
  callbacks: StreamCallback
): Promise<void> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      // Extract error message from response if available
      let errorMessage = `Server error (${response.status})`;
      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorData.message || errorMessage;
      } catch {
        // If response is not JSON, use status text
        errorMessage = response.statusText || errorMessage;
      }

      // Provide user-friendly error messages based on status code
      if (response.status === 429) {
        throw new Error('Too many requests. Please wait a moment and try again.');
      } else if (response.status >= 500) {
        throw new Error('The server is experiencing issues. Please try again later.');
      } else if (response.status === 400) {
        throw new Error(errorMessage || 'Invalid request. Please check your message and try again.');
      } else {
        throw new Error(errorMessage);
      }
    }

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    if (!reader) {
      throw new Error('No response body');
    }

    while (true) {
      const { done, value } = await reader.read();
      
      if (done) {
        callbacks.onComplete();
        break;
      }

      const chunk = decoder.decode(value, { stream: true });
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          
          if (data === '[DONE]') {
            callbacks.onComplete();
            return;
          }

          try {
            const parsed = JSON.parse(data);
            if (parsed.type === 'token' && parsed.content) {
              callbacks.onToken(parsed.content);
            } else if (parsed.type === 'done') {
              callbacks.onComplete();
              return;
            } else if (parsed.type === 'error') {
              callbacks.onError(new Error(parsed.content || 'Unknown error'));
              return;
            }
          } catch (e) {
            // Ignore JSON parse errors for incomplete chunks
            console.debug('Parse error:', e);
          }
        }
      }
    }
  } catch (error) {
    // Check if it's a network error (backend unreachable)
    if (error instanceof TypeError && error.message.includes('fetch')) {
      callbacks.onError(new Error('Unable to connect to the server. Please check your internet connection and try again.'));
    } else {
      callbacks.onError(error as Error);
    }
  }
};

export const getChatHistory = async (sessionId: string): Promise<ChatHistoryResponse> => {
  const response = await apiClient.get<ChatHistoryResponse>(`/api/chat/history/${sessionId}`);
  return response.data;
};

export const deleteChatHistory = async (sessionId: string): Promise<void> => {
  await apiClient.delete(`/api/chat/history/${sessionId}`);
};

export const checkHealth = async () => {
  const response = await apiClient.get('/api/health');
  return response.data;
};
