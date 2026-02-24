import { create } from 'zustand';
import type { ChatState } from '../types';

// Generate UUID without external dependency
const generateUUID = () => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
};

export const useChatStore = create<ChatState>((set) => ({
  sessionId: generateUUID(),
  messages: [],
  isLoading: false,
  error: null,

  addMessage: (message) =>
    set((state) => ({
      messages: [...state.messages, message],
    })),

  updateMessage: (id, content) =>
    set((state) => ({
      messages: state.messages.map((msg) =>
        msg.id === id ? { ...msg, content, isStreaming: false } : msg
      ),
    })),

  setLoading: (loading) =>
    set(() => ({
      isLoading: loading,
    })),

  setError: (error) =>
    set(() => ({
      error,
    })),

  clearMessages: () =>
    set(() => ({
      messages: [],
      error: null,
    })),

  initializeSession: () =>
    set(() => ({
      sessionId: generateUUID(),
      messages: [],
      isLoading: false,
      error: null,
    })),
}));
