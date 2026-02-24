import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, Download, Check } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { Button } from './ui/Button';
import { useScrollThreshold } from '../hooks/useScrollProgress';
import { useReducedMotion } from '../hooks/useReducedMotion';
import { ParticleEffect } from './ParticleEffect';
import { CommandPaletteAvatar } from './CommandPaletteAvatar';
import { smoothScrollTo } from '../utils/scroll';

export const Hero: React.FC = () => {
  const navigate = useNavigate();
  const [downloadState, setDownloadState] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState<string>('');
  
  // Detect if user has scrolled past Hero section
  const isPastHero = useScrollThreshold(window.innerHeight * 0.8);
  
  // Detect reduced motion preference
  const prefersReducedMotion = useReducedMotion();

  const scrollToSection = async (sectionId: string) => {
    try {
      await smoothScrollTo(sectionId);
    } catch (error) {
      // Error already logged in smoothScrollTo, fail silently
    }
  };

  const handleResumeDownload = async () => {
    try {
      setDownloadState('loading');
      setErrorMessage('');
      
      // Check if file exists by attempting to fetch it
      const response = await fetch('/Resume-Rushikesh-Randive-9822929263.pdf', { method: 'HEAD' });
      
      if (!response.ok) {
        throw new Error('Resume file not available');
      }
      
      // Create download link
      const link = document.createElement('a');
      link.href = '/Resume-Rushikesh-Randive-9822929263.pdf';
      link.download = 'Resume-Rushikesh-Randive-9822929263.pdf';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      // Show success state
      setDownloadState('success');
      
      // Reset to idle after 2 seconds
      setTimeout(() => {
        setDownloadState('idle');
      }, 2000);
    } catch (error) {
      setDownloadState('error');
      setErrorMessage('Resume file not available. Please contact me directly.');
      
      // Reset to idle after 3 seconds
      setTimeout(() => {
        setDownloadState('idle');
        setErrorMessage('');
      }, 3000);
    }
  };

  return (
    <section 
      id="hero"
      className="min-h-screen flex items-center justify-center relative overflow-hidden"
      aria-labelledby="hero-heading"
    >
      {/* Animated gradient mesh background with GPU acceleration */}
      {/* Disabled when prefers-reduced-motion enabled */}
      <div 
        className={`absolute inset-0 gradient-mesh ${!prefersReducedMotion ? 'animate-gradient' : ''}`}
        style={{
          willChange: !prefersReducedMotion ? 'background-position' : 'auto',
          transform: 'translateZ(0)',
          backfaceVisibility: 'hidden' as const,
        }}
        aria-hidden="true" 
      />
      
      {/* Subtle particle effects */}
      <ParticleEffect />
      
      {/* Overlay for better text contrast */}
      <div className="absolute inset-0 bg-background/50" aria-hidden="true" />
      
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="max-w-7xl mx-auto">
          {/* Desktop: Left-Right Layout, Mobile: Stacked */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-16 items-center min-h-[calc(100vh-8rem)]">
            
            {/* Left Side: Text Content */}
            <div className="space-y-8 md:space-y-6">
              {/* Status Badge - Available for Opportunities (Requirement 1.4) */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ 
                  duration: 0.5,
                  ease: [0.25, 0.1, 0.25, 1],
                  delay: 0.2 
                }}
                className="flex justify-start"
              >
                <span className="inline-flex items-center px-4 py-2 rounded-full bg-primary/10 border border-primary/30 text-primary font-medium text-sm">
                  <span className="inline-block h-2 w-2 rounded-full bg-primary mr-2 animate-pulse" aria-hidden="true" />
                  Available for Opportunities
                </span>
              </motion.div>

              {/* Main heading (Requirements 1.1, 1.2) */}
              <motion.h1
                id="hero-heading"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3 }}
                className="text-4xl sm:text-5xl md:text-6xl font-bold"
              >
                <motion.span 
                  className="block text-foreground mb-2"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ 
                    duration: 0.5,
                    delay: 0.3
                  }}
                >
                  RUSHIKESH RANDIVE
                </motion.span>
                <motion.span 
                  className="block bg-gradient-to-r from-primary via-purple-400 to-violet-500 bg-clip-text text-transparent"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ 
                    duration: 0.5,
                    delay: 0.5
                  }}
                >
                  FULL STACK DEVELOPER
                </motion.span>
              </motion.h1>

              {/* Headline (Requirement 1.2) */}
              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ 
                  duration: 0.4,
                  ease: [0.25, 0.1, 0.25, 1],
                  delay: 0.8
                }}
                className="text-xl sm:text-2xl md:text-3xl font-semibold text-foreground"
              >
                Building AI-Powered Full Stack Applications
              </motion.p>

              {/* Tagline (Requirement 1.3) */}
              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ 
                  duration: 0.4,
                  ease: [0.25, 0.1, 0.25, 1],
                  delay: 1.0
                }}
                className="text-base sm:text-lg text-muted-foreground leading-relaxed"
              >
                Transforming ideas into production-ready AI systems. Specializing in AI/ML integration, RAG systems, and real-time collaboration features.
              </motion.p>

              {/* Availability (Requirement 1.5) */}
              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ 
                  duration: 0.4,
                  ease: [0.25, 0.1, 0.25, 1],
                  delay: 1.2
                }}
                className="text-sm sm:text-base text-muted-foreground font-medium"
              >
                Remote • Internship • Full-Time Ready
              </motion.p>

              {/* CTA Buttons (Requirements 2.1, 2.2, 2.3) */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ 
                  duration: 0.5,
                  ease: [0.25, 0.1, 0.25, 1],
                  delay: 1.4
                }}
                className="flex flex-col sm:flex-row gap-4"
              >
                <Button
                  size="lg"
                  onClick={() => scrollToSection('projects')}
                  className="text-base sm:text-lg px-8 py-6 shadow-glow hover:shadow-glow-lg transition-all duration-300 hover:scale-105"
                  aria-label="Navigate to projects section"
                >
                  View Projects
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  onClick={handleResumeDownload}
                  disabled={downloadState === 'loading'}
                  className="text-base sm:text-lg px-8 py-6 border-2 hover:border-primary hover:bg-primary/10 transition-all duration-300 hover:scale-105 group relative"
                  aria-label="Download resume"
                >
                  <motion.span
                    className="flex items-center gap-2"
                    animate={downloadState === 'loading' ? { opacity: [1, 0.5, 1] } : {}}
                    transition={{ duration: 1, repeat: downloadState === 'loading' ? Infinity : 0 }}
                  >
                    {downloadState === 'success' ? (
                      <motion.span
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ type: "spring", stiffness: 200, damping: 10 }}
                      >
                        <Check className="h-5 w-5" aria-hidden="true" />
                      </motion.span>
                    ) : (
                      <motion.span
                        whileHover={{ y: 2 }}
                        transition={{ duration: 0.2 }}
                      >
                        <Download className="h-5 w-5 group-hover:animate-bounce" aria-hidden="true" />
                      </motion.span>
                    )}
                    {downloadState === 'loading' ? 'Downloading...' : 
                     downloadState === 'success' ? 'Downloaded!' : 
                     'Download Resume'}
                  </motion.span>
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  onClick={() => navigate('/introduction')}
                  className="text-base sm:text-lg px-8 py-6 border-2 hover:border-primary hover:bg-primary/10 transition-all duration-300 hover:scale-105"
                  aria-label="Navigate to introduction page"
                >
                  Introduction
                </Button>
              </motion.div>

              {/* Error message */}
              <AnimatePresence>
                {errorMessage && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="text-red-500 text-sm"
                    role="alert"
                  >
                    {errorMessage}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* Right Side: CommandPaletteAvatar (Requirements 3.1, 3.4, 3.5) */}
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ 
                duration: 0.6,
                ease: [0.25, 0.1, 0.25, 1],
                delay: 0.4
              }}
              className="order-first md:order-last flex justify-center"
            >
              <CommandPaletteAvatar />
            </motion.div>
          </div>

        </div>

        {/* Scroll indicator - positioned at bottom center */}
        {/* Hide when user scrolls past Hero section */}
        <AnimatePresence>
          {!isPastHero && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.6, delay: 1.2 }}
              className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
            >
              <button
                onClick={() => scrollToSection('experience')}
                className="text-muted-foreground hover:text-primary transition-colors animate-bounce focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 rounded-full p-2"
                aria-label="Scroll to experience section"
              >
                <ChevronDown className="h-6 w-6 sm:h-8 sm:w-8" aria-hidden="true" />
              </button>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </section>
  );
};
