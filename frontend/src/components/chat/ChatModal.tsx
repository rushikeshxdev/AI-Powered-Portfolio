import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';
import { ChatInterface } from './ChatInterface';

interface ChatModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const ChatModal: React.FC<ChatModalProps> = ({ isOpen, onClose }) => {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
            onClick={onClose}
            aria-hidden="true"
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, y: 100, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 100, scale: 0.9 }}
            transition={{ 
              type: "spring",
              stiffness: 300,
              damping: 30
            }}
            className="fixed bottom-24 right-6 z-50 w-[calc(100vw-3rem)] sm:w-[450px] max-h-[600px] glassmorphism rounded-2xl shadow-2xl overflow-hidden"
            role="dialog"
            aria-modal="true"
            aria-labelledby="chat-modal-title"
          >
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-border bg-card/80">
              <h2 id="chat-modal-title" className="text-lg font-semibold flex items-center gap-2">
                <span className="text-primary">▸</span> AI Assistant
              </h2>
              <button
                onClick={onClose}
                className="p-2 rounded-lg hover:bg-muted transition-colors focus:outline-none focus:ring-2 focus:ring-primary"
                aria-label="Close chat"
              >
                <X className="h-5 w-5" aria-hidden="true" />
              </button>
            </div>

            {/* Chat Content */}
            <div className="h-[500px] overflow-hidden">
              <ChatInterface isModal />
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};
