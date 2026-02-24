import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useReducedMotion } from '../hooks/useReducedMotion';

/**
 * CommandPaletteAvatar Component
 * 
 * Terminal/command palette style interface with animated typing effect.
 * Cycles through developer commands showing personal information.
 * Respects reduced motion preferences for accessibility.
 */

interface Command {
  input: string;
  output: string;
}

const commands: Command[] = [
  { input: '> whoami', output: 'Rushikesh Randive' },
  { input: '> role', output: 'Full Stack Developer' },
  { input: '> specialization', output: 'AI-Powered Applications' },
  { input: '> status', output: 'Available for Opportunities' },
];

export const CommandPaletteAvatar: React.FC = () => {
  const [currentCommandIndex, setCurrentCommandIndex] = useState(0);
  const [displayedInput, setDisplayedInput] = useState('');
  const [displayedOutput, setDisplayedOutput] = useState('');
  const [phase, setPhase] = useState<'typing-input' | 'typing-output' | 'display'>('typing-input');
  const prefersReducedMotion = useReducedMotion();

  const currentCommand = commands[currentCommandIndex];

  useEffect(() => {
    if (prefersReducedMotion) {
      // Skip animations, show final state immediately
      setDisplayedInput(currentCommand.input);
      setDisplayedOutput(currentCommand.output);
      setPhase('display');
      
      const timer = setTimeout(() => {
        setCurrentCommandIndex((prev) => (prev + 1) % commands.length);
        setDisplayedInput('');
        setDisplayedOutput('');
        setPhase('typing-input');
      }, 4000);
      
      return () => clearTimeout(timer);
    }

    let timeoutId: ReturnType<typeof setTimeout>;

    if (phase === 'typing-input') {
      // Type out the input command
      if (displayedInput.length < currentCommand.input.length) {
        timeoutId = setTimeout(() => {
          setDisplayedInput(currentCommand.input.slice(0, displayedInput.length + 1));
        }, 50); // 50ms per character
      } else {
        // Input complete, move to output phase
        timeoutId = setTimeout(() => {
          setPhase('typing-output');
        }, 300);
      }
    } else if (phase === 'typing-output') {
      // Type out the output
      if (displayedOutput.length < currentCommand.output.length) {
        timeoutId = setTimeout(() => {
          setDisplayedOutput(currentCommand.output.slice(0, displayedOutput.length + 1));
        }, 50); // 50ms per character
      } else {
        // Output complete, display for a moment
        timeoutId = setTimeout(() => {
          setPhase('display');
        }, 300);
      }
    } else if (phase === 'display') {
      // Display complete command for 2 seconds before moving to next
      timeoutId = setTimeout(() => {
        setCurrentCommandIndex((prev) => (prev + 1) % commands.length);
        setDisplayedInput('');
        setDisplayedOutput('');
        setPhase('typing-input');
      }, 2000);
    }

    return () => clearTimeout(timeoutId);
  }, [phase, displayedInput, displayedOutput, currentCommand, currentCommandIndex, prefersReducedMotion]);

  return (
    <div className="w-full max-w-2xl mx-auto">
      {/* Terminal Window */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: prefersReducedMotion ? 0 : 0.6, ease: [0.25, 0.1, 0.25, 1] }}
        className="relative"
      >
        {/* Glow effect */}
        <div 
          className="absolute inset-0 bg-gradient-to-br from-primary/20 via-purple-500/20 to-violet-500/20 blur-3xl"
          aria-hidden="true"
        />

        {/* Terminal container */}
        <div className="relative bg-[#0A0A0A] rounded-lg shadow-2xl border border-primary/30 overflow-hidden">
          {/* Terminal header */}
          <div className="bg-[#1A1A1A] px-4 py-3 flex items-center gap-2 border-b border-primary/20">
            <div className="flex gap-2">
              <div 
                className="w-3 h-3 rounded-full bg-[#FF5F56]"
                aria-label="Close"
                role="button"
                tabIndex={-1}
              />
              <div 
                className="w-3 h-3 rounded-full bg-[#FFBD2E]"
                aria-label="Minimize"
                role="button"
                tabIndex={-1}
              />
              <div 
                className="w-3 h-3 rounded-full bg-[#27C93F]"
                aria-label="Maximize"
                role="button"
                tabIndex={-1}
              />
            </div>
            <div className="flex-1 text-center">
              <span className="text-xs text-gray-400 font-mono">terminal</span>
            </div>
          </div>

          {/* Terminal content */}
          <div 
            className="p-6 font-mono text-sm sm:text-base min-h-[200px] sm:min-h-[250px]"
            role="log"
            aria-live="polite"
            aria-label="Terminal output"
          >
            {/* Command input line */}
            <div className="mb-2">
              <span className="text-[#6B46C1]" aria-label="Command prompt">
                {displayedInput}
              </span>
              {phase === 'typing-input' && (
                <motion.span
                  className="inline-block w-2 h-4 bg-[#6B46C1] ml-1"
                  animate={prefersReducedMotion ? {} : { opacity: [1, 0, 1] }}
                  transition={{ duration: 0.8, repeat: Infinity, ease: 'linear' }}
                  aria-hidden="true"
                />
              )}
            </div>

            {/* Command output */}
            <AnimatePresence mode="wait">
              {displayedOutput && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: prefersReducedMotion ? 0 : 0.2 }}
                  className="mb-4"
                >
                  <span className="text-gray-300">
                    {displayedOutput}
                  </span>
                  {phase === 'typing-output' && (
                    <motion.span
                      className="inline-block w-2 h-4 bg-gray-300 ml-1"
                      animate={prefersReducedMotion ? {} : { opacity: [1, 0, 1] }}
                      transition={{ duration: 0.8, repeat: Infinity, ease: 'linear' }}
                      aria-hidden="true"
                    />
                  )}
                </motion.div>
              )}
            </AnimatePresence>

            {/* Cursor on new line when in display phase */}
            {phase === 'display' && (
              <div>
                <span className="text-[#6B46C1]">{'>'}</span>
                <motion.span
                  className="inline-block w-2 h-4 bg-[#6B46C1] ml-1"
                  animate={prefersReducedMotion ? {} : { opacity: [1, 0, 1] }}
                  transition={{ duration: 0.8, repeat: Infinity, ease: 'linear' }}
                  aria-hidden="true"
                />
              </div>
            )}
          </div>
        </div>

        {/* Progress indicator dots */}
        <div className="flex justify-center gap-2 mt-4" role="tablist" aria-label="Command progress">
          {commands.map((_, index) => (
            <motion.div
              key={index}
              className={`w-2 h-2 rounded-full transition-colors duration-300 ${
                index === currentCommandIndex ? 'bg-primary' : 'bg-primary/30'
              }`}
              animate={
                index === currentCommandIndex && !prefersReducedMotion
                  ? { scale: [1, 1.2, 1] }
                  : {}
              }
              transition={{ duration: 0.6, repeat: Infinity }}
              role="tab"
              aria-selected={index === currentCommandIndex}
              aria-label={`Command ${index + 1}`}
            />
          ))}
        </div>
      </motion.div>
    </div>
  );
};
