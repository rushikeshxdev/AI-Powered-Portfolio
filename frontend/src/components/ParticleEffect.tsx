/**
 * Subtle particle effect for Hero section background
 * GPU-accelerated using transform and opacity (Requirements 5.3, 20.1)
 * Disabled when prefers-reduced-motion enabled (Requirements 5.4, 21.3)
 * Optimized for 30fps+ rendering (Requirement 5.2)
 */

import React, { useMemo } from 'react';
import { motion } from 'framer-motion';
import { useReducedMotion } from '../hooks/useReducedMotion';

interface Particle {
  id: number;
  x: number;
  y: number;
  size: number;
  duration: number;
  delay: number;
}

export const ParticleEffect: React.FC = () => {
  const prefersReducedMotion = useReducedMotion();

  // Generate particles only once
  const particles = useMemo<Particle[]>(() => {
    const particleCount = 20; // Keep count low for performance
    return Array.from({ length: particleCount }, (_, i) => ({
      id: i,
      x: Math.random() * 100, // Random x position (%)
      y: Math.random() * 100, // Random y position (%)
      size: Math.random() * 3 + 1, // Size between 1-4px
      duration: Math.random() * 10 + 15, // Duration between 15-25s
      delay: Math.random() * 5, // Delay between 0-5s
    }));
  }, []);

  // Don't render particles if reduced motion is preferred
  if (prefersReducedMotion) {
    return null;
  }

  return (
    <div 
      className="absolute inset-0 overflow-hidden pointer-events-none"
      aria-hidden="true"
    >
      {particles.map((particle) => (
        <motion.div
          key={particle.id}
          className="absolute rounded-full bg-primary/20"
          style={{
            left: `${particle.x}%`,
            top: `${particle.y}%`,
            width: `${particle.size}px`,
            height: `${particle.size}px`,
            // GPU acceleration hints (Requirements 20.1, 20.5)
            willChange: 'transform, opacity',
            transform: 'translateZ(0)',
            backfaceVisibility: 'hidden' as const,
          }}
          animate={{
            // Subtle floating animation using GPU-accelerated properties
            y: [0, -30, 0],
            x: [0, Math.random() * 20 - 10, 0],
            opacity: [0.2, 0.5, 0.2],
            scale: [1, 1.2, 1],
          }}
          transition={{
            duration: particle.duration,
            delay: particle.delay,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        />
      ))}
    </div>
  );
};
