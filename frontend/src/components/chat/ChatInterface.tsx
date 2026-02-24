import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useChatStore } from '../../stores/chatStore';
import { sendChatMessage, deleteChatHistory } from '../../api/client';
import { ChatMessages } from './ChatMessages';
import { ChatInput } from './ChatInput';
import { SuggestedQuestions } from './SuggestedQuestions';
import { Button } from '../ui/Button';
import type { Message } from '../../types';

interface ChatInterfaceProps {
  isModal?: boolean;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({ isModal: _isModal = false }) => {
  const {
    sessionId,
    messages,
    isLoading,
    error,
    addMessage,
    updateMessage,
    setLoading,
    setError,
    clearMessages,
  } = useChatStore();

  const [showSuggestions, setShowSuggestions] = useState(true);
  const [lastFailedMessage, setLastFailedMessage] = useState<string | null>(null);

  const generateMessageId = () => {
    return `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  };

  const handleSendMessage = async (content: string) => {
    if (!content.trim() || isLoading) return;

    // Hide suggestions after first message
    setShowSuggestions(false);

    // Clear any previous error
    setError(null);
    setLastFailedMessage(null);

    // Add user message
    const userMessage: Message = {
      id: generateMessageId(),
      role: 'user',
      content,
      timestamp: new Date(),
    };
    addMessage(userMessage);

    // Create assistant message placeholder
    const assistantMessageId = generateMessageId();
    const assistantMessage: Message = {
      id: assistantMessageId,
      role: 'assistant',
      content: '',
      timestamp: new Date(),
      isStreaming: true,
    };
    addMessage(assistantMessage);

    setLoading(true);

    try {
      let accumulatedContent = '';

      await sendChatMessage(
        {
          question: content,
          session_id: sessionId,
        },
        {
          onToken: (token: string) => {
            accumulatedContent += token;
            updateMessage(assistantMessageId, accumulatedContent);
          },
          onComplete: () => {
            setLoading(false);
            updateMessage(assistantMessageId, accumulatedContent);
          },
          onError: (error: Error) => {
            setLoading(false);
            setError(error.message);
            setLastFailedMessage(content);
            updateMessage(
              assistantMessageId,
              `Sorry, I encountered an error: ${error.message}`
            );
          },
        }
      );
    } catch (error) {
      setLoading(false);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
      setError(errorMessage);
      setLastFailedMessage(content);
      updateMessage(
        assistantMessageId,
        `Sorry, I encountered an error: ${errorMessage}`
      );
    }
  };

  const handleRetry = () => {
    if (lastFailedMessage) {
      handleSendMessage(lastFailedMessage);
    }
  };

  const handleClearHistory = async () => {
    try {
      await deleteChatHistory(sessionId);
      clearMessages();
      setShowSuggestions(true);
      setError(null);
      setLastFailedMessage(null);
    } catch (error) {
      console.error('Failed to clear history:', error);
      // Still clear locally even if API call fails
      clearMessages();
      setShowSuggestions(true);
      setError(null);
      setLastFailedMessage(null);
    }
  };

  const handleQuestionClick = (question: string) => {
    handleSendMessage(question);
  };

  return (
    <section 
      id="chat" 
      className="py-12 sm:py-16 md:py-20 relative overflow-hidden"
      aria-labelledby="chat-heading"
    >
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-background to-purple-500/5" aria-hidden="true" />
      
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h2 id="chat-heading" className="text-3xl sm:text-4xl font-bold text-center mb-3 sm:mb-4">
            Chat with AI
          </h2>
          <p className="text-sm sm:text-base text-center text-muted-foreground mb-6 sm:mb-8 max-w-2xl mx-auto px-4">
            Ask me anything about Rushikesh's background, skills, projects, or experience.
            I'm powered by AI and have access to his complete resume.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="max-w-4xl mx-auto"
        >
          <div className="glassmorphism rounded-2xl shadow-2xl overflow-hidden">
            <div 
              className="flex flex-col h-[500px] sm:h-[600px] overflow-y-auto"
              role="region"
              aria-label="AI chat interface"
            >
              {/* Suggested Questions */}
              {showSuggestions && messages.length === 0 && (
                <div className="p-3 sm:p-4 border-b border-border/50">
                  <SuggestedQuestions onQuestionClick={handleQuestionClick} />
                </div>
              )}

              {/* Messages */}
              <ChatMessages messages={messages} isLoading={isLoading} />

              {/* Error Display */}
              {error && (
                <div 
                  className="px-3 sm:px-4 py-3 bg-destructive/10 border-t border-destructive/20 backdrop-blur-sm"
                  role="alert"
                  aria-live="assertive"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex-1">
                      <p className="text-destructive text-xs sm:text-sm font-medium mb-1">
                        Error
                      </p>
                      <p className="text-destructive/90 text-xs sm:text-sm">
                        {error}
                      </p>
                    </div>
                    {lastFailedMessage && (
                      <Button
                        onClick={handleRetry}
                        disabled={isLoading}
                        variant="outline"
                        size="sm"
                        className="shrink-0 border-destructive/30 text-destructive hover:bg-destructive/10"
                        aria-label="Retry failed message"
                      >
                        Retry
                      </Button>
                    )}
                  </div>
                </div>
              )}

              {/* Input */}
              <ChatInput
                onSendMessage={handleSendMessage}
                onClearHistory={handleClearHistory}
                isLoading={isLoading}
              />
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};
