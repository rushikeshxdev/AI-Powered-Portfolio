import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useReducedMotion } from '../hooks/useReducedMotion';

/**
 * VoxelAvatar Component
 * 
 * Displays an animated avatar using the user's profile picture.
 * Supports four animation states: idle, typing, thinking, wave
 * Respects reduced motion preferences for accessibility.
 * 
 * Requirements: 3.1, 3.2, 3.3, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7
 */

export type AnimationState = 'idle' | 'typing' | 'thinking' | 'wave';

export interface VoxelAvatarProps {
  className?: string;
  animationState?: AnimationState;
  autoAnimate?: boolean; // Enable automatic state cycling
}

export const VoxelAvatar: React.FC<VoxelAvatarProps> = ({
  className = '',
  animationState = 'idle',
  autoAnimate = true,
}) => {
  const [currentState, setCurrentState] = useState<AnimationState>(animationState);
  const prefersReducedMotion = useReducedMotion();

  // Auto-cycle through animation states with random transitions (Requirement 4.6)
  useEffect(() => {
    if (!autoAnimate || prefersReducedMotion) {
      return;
    }

    const states: AnimationState[] = ['idle', 'typing', 'thinking', 'wave'];
    let timeoutId: ReturnType<typeof setTimeout>;
    
    const scheduleNextTransition = () => {
      // Random interval between 5-10 seconds (5000-10000ms)
      const randomInterval = Math.floor(Math.random() * 5000) + 5000;
      
      timeoutId = setTimeout(() => {
        setCurrentState((prev) => {
          // Get a random state different from the current one
          const availableStates = states.filter(s => s !== prev);
          const randomIndex = Math.floor(Math.random() * availableStates.length);
          return availableStates[randomIndex];
        });
        
        // Schedule the next transition
        scheduleNextTransition();
      }, randomInterval);
    };

    scheduleNextTransition();

    return () => clearTimeout(timeoutId);
  }, [autoAnimate, prefersReducedMotion]);

  // Update state when prop changes
  useEffect(() => {
    if (!autoAnimate) {
      setCurrentState(animationState);
    }
  }, [animationState, autoAnimate]);

  // Animation variants for different states (Requirements 4.2, 4.3, 4.4, 4.5)
  const getAnimationVariants = () => {
    if (prefersReducedMotion) {
      // Static pose when reduced motion is enabled (Requirement 4.7)
      return {
        idle: { scale: 1, rotate: 0, y: 0 },
        typing: { scale: 1, rotate: 0, y: 0 },
        thinking: { scale: 1, rotate: 0, y: 0 },
        wave: { scale: 1, rotate: 0, y: 0 },
      };
    }

    return {
      // Idle: Subtle breathing/bobbing motion (Requirement 4.2)
      idle: {
        y: [0, -10, 0],
        scale: [1, 1.02, 1],
        transition: {
          duration: 3,
          repeat: Infinity,
          ease: [0.42, 0, 0.58, 1] as const,
        },
      },
      // Typing: Slight forward lean and subtle shake (Requirement 4.3)
      typing: {
        rotate: [0, -2, 2, -2, 0],
        scale: [1, 0.98, 1.02, 0.98, 1],
        transition: {
          duration: 2,
          repeat: Infinity,
          ease: [0.42, 0, 0.58, 1] as const,
        },
      },
      // Thinking: Slight tilt and pause (Requirement 4.4)
      thinking: {
        rotate: [0, 5, 5, 0],
        y: [0, -5, -5, 0],
        transition: {
          duration: 4,
          repeat: Infinity,
          ease: [0.42, 0, 0.58, 1] as const,
        },
      },
      // Wave: Gentle rocking motion (Requirement 4.5)
      wave: {
        rotate: [0, -10, 10, -10, 0],
        scale: [1, 1.05, 1, 1.05, 1],
        transition: {
          duration: 1.5,
          repeat: Infinity,
          ease: [0.42, 0, 0.58, 1] as const,
        },
      },
    };
  };

  const variants = getAnimationVariants();

  // Container animation for 3D perspective effect
  const containerVariants = {
    initial: { opacity: 0, scale: 0.8 },
    animate: { 
      opacity: 1, 
      scale: 1,
      transition: {
        duration: prefersReducedMotion ? 0 : 0.6,
        ease: [0.25, 0.1, 0.25, 1] as const,
      },
    },
  };

  return (
    <div 
      className={`relative flex items-center justify-center ${className}`}
      style={{
        perspective: '1000px',
        transformStyle: 'preserve-3d',
      }}
    >
      {/* 3D Container with perspective (Requirement 3.3) */}
      <motion.div
        variants={containerVariants}
        initial="initial"
        animate="animate"
        className="relative"
      >
        {/* Avatar Image with Animation */}
        <motion.div
          animate={variants[currentState]}
          className="relative"
          style={{
            transformStyle: 'preserve-3d',
          }}
        >
          {/* Main Avatar Image */}
          <div className="relative w-64 h-64 md:w-80 md:h-80 lg:w-96 lg:h-96">
            {/* Glow effect background (purple theme) */}
            <div 
              className="absolute inset-0 rounded-xl bg-gradient-to-br from-primary/30 via-purple-500/30 to-violet-500/30 blur-2xl"
              style={{
                transform: 'translateZ(-20px)',
              }}
              aria-hidden="true"
            />
            
            {/* Avatar container with border - Square with rounded corners */}
            <div className="relative w-full h-full rounded-xl overflow-hidden border-4 border-primary/50 shadow-2xl shadow-primary/20">
              <img
                src="/avatar.jpg"
                alt="Rushikesh Randive - Full Stack Developer"
                className="w-full h-full object-cover"
                loading="eager"
              />
              
              {/* Overlay gradient for terminal aesthetic */}
              <div 
                className="absolute inset-0 bg-gradient-to-br from-primary/10 via-transparent to-purple-500/10 mix-blend-overlay"
                aria-hidden="true"
              />
            </div>

            {/* Animated ring indicator */}
            {!prefersReducedMotion && (
              <motion.div
                className="absolute inset-0 rounded-xl border-2 border-primary/30"
                animate={{
                  scale: [1, 1.1, 1],
                  opacity: [0.5, 0.2, 0.5],
                }}
                transition={{
                  duration: 3,
                  repeat: Infinity,
                  ease: 'easeInOut',
                }}
                aria-hidden="true"
              />
            )}
          </div>

          {/* State Indicator Badge */}
          <AnimatePresence mode="wait">
            <motion.div
              key={currentState}
              initial={{ opacity: 0, y: 10, scale: 0.8 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -10, scale: 0.8 }}
              transition={{ duration: prefersReducedMotion ? 0 : 0.3 }}
              className="absolute -bottom-4 left-1/2 transform -translate-x-1/2 px-4 py-2 rounded-full bg-background/90 backdrop-blur-sm border border-primary/30 shadow-lg"
            >
              <span className="text-sm font-mono text-primary flex items-center gap-2">
                <span 
                  className={`inline-block h-2 w-2 rounded-full bg-primary ${!prefersReducedMotion ? 'animate-pulse' : ''}`}
                  aria-hidden="true"
                />
                {currentState}
              </span>
            </motion.div>
          </AnimatePresence>
        </motion.div>
      </motion.div>

      {/* Decorative particles (disabled with reduced motion) */}
      {!prefersReducedMotion && (
        <>
          <motion.div
            className="absolute top-1/4 left-1/4 w-2 h-2 rounded-full bg-primary/40"
            animate={{
              y: [-20, 20, -20],
              x: [-10, 10, -10],
              opacity: [0.2, 0.6, 0.2],
            }}
            transition={{
              duration: 4,
              repeat: Infinity,
              ease: 'easeInOut',
            }}
            aria-hidden="true"
          />
          <motion.div
            className="absolute bottom-1/4 right-1/4 w-3 h-3 rounded-full bg-cyan-500/40"
            animate={{
              y: [20, -20, 20],
              x: [10, -10, 10],
              opacity: [0.3, 0.7, 0.3],
            }}
            transition={{
              duration: 5,
              repeat: Infinity,
              ease: 'easeInOut',
              delay: 1,
            }}
            aria-hidden="true"
          />
        </>
      )}
    </div>
  );
};
