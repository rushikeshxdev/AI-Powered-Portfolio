import React from 'react';
import { motion } from 'framer-motion';

const suggestedQuestions = [
  "What projects has Rushikesh worked on?",
  "Tell me about Rushikesh's experience with AI and LLMs",
  "What technologies is Rushikesh proficient in?",
  "Describe Rushikesh's education background",
  "What is Rushikesh's current role?",
  "Has Rushikesh worked with React and TypeScript?",
  "What backend technologies does Rushikesh know?",
];

export const SuggestedQuestions: React.FC<{ onQuestionClick: (question: string) => void }> = ({
  onQuestionClick,
}) => {
  return (
    <div className="mb-3 sm:mb-4">
      <p className="text-xs sm:text-sm text-muted-foreground mb-2" id="suggested-questions-label">
        Suggested questions:
      </p>
      <div 
        className="flex flex-wrap gap-1.5 sm:gap-2 overflow-x-auto pb-2"
        role="list"
        aria-labelledby="suggested-questions-label"
      >
        {suggestedQuestions.map((question, index) => (
          <motion.button
            key={index}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.05 }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => onQuestionClick(question)}
            className="text-[11px] sm:text-xs bg-secondary text-secondary-foreground px-2.5 sm:px-3 py-1.5 sm:py-2 rounded-full hover:bg-primary hover:text-primary-foreground transition-colors whitespace-nowrap focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
            role="listitem"
            aria-label={`Ask: ${question}`}
          >
            {question}
          </motion.button>
        ))}
      </div>
    </div>
  );
};
