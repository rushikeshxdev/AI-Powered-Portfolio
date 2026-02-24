import React, { useState, type KeyboardEvent } from 'react';
import { Send, Trash2 } from 'lucide-react';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  onClearHistory: () => void;
  isLoading: boolean;
  disabled?: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({
  onSendMessage,
  onClearHistory,
  isLoading,
  disabled = false,
}) => {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim() && !isLoading && !disabled) {
      onSendMessage(input.trim());
      setInput('');
    }
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleClear = () => {
    if (window.confirm('Are you sure you want to clear the chat history?')) {
      onClearHistory();
    }
  };

  return (
    <div className="border-t border-border p-3 sm:p-4 bg-background">
      <form 
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        className="flex gap-2"
        role="search"
        aria-label="Chat message form"
      >
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask me anything about Rushikesh's background..."
          disabled={isLoading || disabled}
          className="flex-1 text-sm sm:text-base"
          maxLength={500}
          aria-label="Type your message here"
          aria-describedby="char-count"
          aria-required="true"
        />
        <Button
          type="submit"
          disabled={!input.trim() || isLoading || disabled}
          size="default"
          aria-label={isLoading ? "Sending message..." : "Send message"}
          className="shrink-0"
        >
          <Send className="h-4 w-4" aria-hidden="true" />
          <span className="sr-only sm:not-sr-only sm:ml-2">Send</span>
        </Button>
        <Button
          type="button"
          onClick={handleClear}
          disabled={isLoading}
          variant="outline"
          size="default"
          aria-label="Clear chat history"
          className="shrink-0"
        >
          <Trash2 className="h-4 w-4" aria-hidden="true" />
          <span className="sr-only">Clear</span>
        </Button>
      </form>
      {input.length > 450 && (
        <p id="char-count" className="text-xs text-muted-foreground mt-1" role="status" aria-live="polite">
          {500 - input.length} characters remaining
        </p>
      )}
    </div>
  );
};
