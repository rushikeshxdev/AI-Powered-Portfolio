/**
 * ScrollProgress Component
 * 
 * Displays a fixed progress bar at the top of the page showing scroll progress
 * Updates in real-time with max 50ms delay (Requirement 13.2, Property 26)
 * 
 * Requirements:
 * - 13.1: Display scroll progress indicator showing percentage of page scrolled
 * - 13.2: Update progress indicator in real-time
 * - 13.3: Visible and positioned consistently during scroll
 * - 13.4: Smooth animation with max 50ms update delay
 */

import React from 'react';
import { motion } from 'framer-motion';
import { useScrollProgress } from '../hooks/useScrollProgress';
import { useReducedMotion } from '../hooks/useReducedMotion';

export const ScrollProgress: React.FC = () => {
  const progress = useScrollProgress();
  const prefersReducedMotion = useReducedMotion();

  return (
    <motion.div
      className="fixed top-0 left-0 right-0 h-1 bg-gray-200 dark:bg-gray-800 z-50"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ 
        delay: 0.5,
        duration: prefersReducedMotion ? 0.1 : 0.3 
      }}
      role="progressbar"
      aria-label="Page scroll progress"
      aria-valuenow={Math.round(progress)}
      aria-valuemin={0}
      aria-valuemax={100}
    >
      <motion.div
        className="h-full bg-gradient-to-r from-primary to-green-400"
        style={{ width: `${progress}%` }}
        transition={{ 
          duration: prefersReducedMotion ? 0 : 0.05, // Max 50ms update delay
          ease: 'linear'
        }}
      />
    </motion.div>
  );
};
