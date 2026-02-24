import React, { useState, lazy, Suspense } from 'react';
import { Bot, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from './ui/Button';
import { Skeleton } from './ui/Skeleton';
import { pulseAnimation, scaleOnHover } from '../utils/animations';
import { useReducedMotion } from '../hooks/useReducedMotion';

const ChatInterface = lazy(() => import('./chat/ChatInterface').then(module => ({ default: module.ChatInterface })));

export const FloatingChatbot: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const prefersReducedMotion = useReducedMotion();

  return (
    <>
      {/* Floating Button */}
      <motion.div
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ delay: 1, type: "spring", stiffness: 260, damping: 20 }}
        className="fixed bottom-6 right-6 z-50"
      >
        <Button
          size="lg"
          onClick={() => setIsOpen(!isOpen)}
          className="h-14 w-14 rounded-full shadow-glow-lg hover:shadow-glow transition-all duration-300 hover:scale-110"
          aria-label={isOpen ? "Close chat" : "Open chat"}
        >
          {isOpen ? (
            <X className="h-6 w-6" aria-hidden="true" />
          ) : (
            <motion.div
              variants={pulseAnimation}
              initial="initial"
              animate={prefersReducedMotion ? "initial" : "animate"}
              className="relative"
            >
              <motion.div
                variants={scaleOnHover}
                initial="rest"
                whileHover="hover"
                transition={{ duration: 0.2 }}
              >
                <Bot className="h-6 w-6" aria-hidden="true" data-testid="bot-icon" />
              </motion.div>
            </motion.div>
          )}
        </Button>
      </motion.div>

      {/* Chat Modal */}
      <AnimatePresence>
        {isOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsOpen(false)}
              className="fixed inset-0 bg-background/80 backdrop-blur-sm z-40"
              aria-hidden="true"
            />

            {/* Chat Container */}
            <motion.div
              initial={{ opacity: 0, y: 100, scale: 0.9 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 100, scale: 0.9 }}
              transition={{ type: "spring", stiffness: 300, damping: 30 }}
              className="fixed bottom-24 right-6 w-[calc(100vw-3rem)] sm:w-[450px] h-[600px] max-h-[calc(100vh-8rem)] z-50"
            >
              <div className="glassmorphism rounded-2xl shadow-2xl h-full flex flex-col overflow-hidden border-2 border-primary/20">
                {/* Header */}
                <div className="bg-gradient-to-r from-primary to-primary/80 text-primary-foreground px-6 py-4 flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="h-10 w-10 rounded-full bg-primary-foreground/20 flex items-center justify-center">
                      <Bot className="h-5 w-5" aria-hidden="true" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-lg">AI Assistant</h3>
                      <p className="text-xs text-primary-foreground/80">Ask me anything!</p>
                    </div>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setIsOpen(false)}
                    className="text-primary-foreground hover:bg-primary-foreground/20"
                    aria-label="Close chat"
                  >
                    <X className="h-5 w-5" aria-hidden="true" />
                  </Button>
                </div>

                {/* Chat Content */}
                <div className="flex-1 overflow-hidden">
                  <Suspense fallback={
                    <div className="p-6 space-y-4">
                      <Skeleton className="h-20 w-full" />
                      <Skeleton className="h-20 w-3/4" />
                      <Skeleton className="h-20 w-full" />
                    </div>
                  }>
                    <ChatInterface />
                  </Suspense>
                </div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
};
