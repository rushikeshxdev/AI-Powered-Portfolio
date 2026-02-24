import React from 'react';
import { motion } from 'framer-motion';
import { User, Bot } from 'lucide-react';
import type { MessageBubbleProps } from '../../types';

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user';

  const formatTime = (date: Date) => {
    return new Date(date).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex gap-2 sm:gap-3 mb-3 sm:mb-4 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}
      role="article"
      aria-label={`Message from ${isUser ? 'you' : 'AI assistant'} at ${formatTime(message.timestamp)}`}
    >
      {/* Avatar */}
      <div
        className={`flex-shrink-0 w-7 h-7 sm:w-8 sm:h-8 rounded-full flex items-center justify-center ${
          isUser ? 'bg-primary' : 'bg-secondary'
        }`}
        aria-hidden="true"
        role="img"
        aria-label={isUser ? 'User avatar' : 'AI assistant avatar'}
      >
        {isUser ? (
          <User className="h-4 w-4 sm:h-5 sm:w-5 text-primary-foreground" />
        ) : (
          <Bot className="h-4 w-4 sm:h-5 sm:w-5 text-secondary-foreground" />
        )}
      </div>

      {/* Message Content */}
      <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} max-w-[85%] sm:max-w-[80%]`}>
        <div
          className={`rounded-lg px-3 py-2 sm:px-4 sm:py-2 ${
            isUser
              ? 'bg-primary text-primary-foreground'
              : 'bg-muted text-muted-foreground'
          }`}
        >
          <p className="text-xs sm:text-sm whitespace-pre-wrap break-words">
            {message.content}
            {message.isStreaming && (
              <span className="inline-block w-2 h-4 ml-1 bg-current animate-pulse" aria-label="Message is being typed" role="status" />
            )}
          </p>
        </div>
        <time className="text-[10px] sm:text-xs text-muted-foreground mt-1" dateTime={message.timestamp.toISOString()}>
          {formatTime(message.timestamp)}
        </time>
      </div>
    </motion.div>
  );
};
