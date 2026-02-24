import { useEffect, useLayoutEffect, useRef } from 'react';
import { MessageBubble } from './MessageBubble';
import { MessageSkeleton } from '../ui/Skeleton';
import type { Message } from '../../types';

interface ChatMessagesProps {
  messages: Message[];
  isLoading: boolean;
}

export const ChatMessages: React.FC<ChatMessagesProps> = ({ messages, isLoading }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messagesContainerRef = useRef<HTMLDivElement>(null);

  // Get the last message content to trigger scroll during streaming
  const lastMessageContent = messages[messages.length - 1]?.content || '';

  const scrollToBottom = (behavior: ScrollBehavior = 'smooth') => {
    messagesEndRef.current?.scrollIntoView({ behavior });
  };

  // Scroll on messages change
  useEffect(() => {
    scrollToBottom('smooth');
  }, [messages.length]); // Only on new messages

  // Scroll during streaming (instant)
  useLayoutEffect(() => {
    if (isLoading || messages.some(m => m.isStreaming)) {
      scrollToBottom('auto'); // Instant scroll during streaming
    }
  }, [lastMessageContent, isLoading]); // Triggers on content updates

  return (
    <div 
      ref={messagesContainerRef}
      className="flex-1 overflow-y-auto p-3 sm:p-4 space-y-3 sm:space-y-4"
      role="log"
      aria-live="polite"
      aria-atomic="false"
      aria-relevant="additions"
      aria-label="Chat conversation"
    >
      {messages.length === 0 ? (
        <div className="flex items-center justify-center h-full text-muted-foreground" role="status">
          <div className="text-center px-4">
            <p className="text-base sm:text-lg mb-2">👋 Hi! I'm an AI assistant.</p>
            <p className="text-xs sm:text-sm">Ask me anything about Rushikesh's background, skills, or projects!</p>
          </div>
        </div>
      ) : (
        <>
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
          {isLoading && (
            <MessageSkeleton />
          )}
        </>
      )}
      <div ref={messagesEndRef} />
    </div>
  );
};
