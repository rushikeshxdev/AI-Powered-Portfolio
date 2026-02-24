/**
 * Hook to track scroll progress through the page
 * Updates in real-time with max 50ms delay (Requirement 13.2, Property 26)
 * Returns progress as percentage (0-100)
 */

import { useEffect, useState } from 'react';

export const useScrollProgress = (): number => {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    // Calculate scroll progress as percentage
    const updateProgress = () => {
      // Total scrollable height
      const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
      
      // Current scroll position
      const scrolled = window.scrollY;
      
      // Calculate percentage (0-100)
      const progress = scrollHeight > 0 ? (scrolled / scrollHeight) * 100 : 0;
      
      // Ensure progress is between 0 and 100
      setProgress(Math.min(Math.max(progress, 0), 100));
    };

    // Add scroll listener with passive flag for better performance
    // Passive listeners don't block scrolling (Requirement 20.3)
    window.addEventListener('scroll', updateProgress, { passive: true });
    
    // Calculate initial progress
    updateProgress();

    // Cleanup
    return () => window.removeEventListener('scroll', updateProgress);
  }, []);

  return progress;
};

/**
 * Hook to detect if user has scrolled past a certain threshold
 * Useful for showing/hiding elements based on scroll position
 */
export const useScrollThreshold = (threshold: number = 100): boolean => {
  const [isPastThreshold, setIsPastThreshold] = useState(false);

  useEffect(() => {
    const checkThreshold = () => {
      setIsPastThreshold(window.scrollY > threshold);
    };

    window.addEventListener('scroll', checkThreshold, { passive: true });
    checkThreshold();

    return () => window.removeEventListener('scroll', checkThreshold);
  }, [threshold]);

  return isPastThreshold;
};

/**
 * Hook to detect scroll direction
 * Returns 'up', 'down', or null
 */
export const useScrollDirection = (): 'up' | 'down' | null => {
  const [scrollDirection, setScrollDirection] = useState<'up' | 'down' | null>(null);
  const [lastScrollY, setLastScrollY] = useState(0);

  useEffect(() => {
    const updateScrollDirection = () => {
      const currentScrollY = window.scrollY;
      
      if (currentScrollY > lastScrollY) {
        setScrollDirection('down');
      } else if (currentScrollY < lastScrollY) {
        setScrollDirection('up');
      }
      
      setLastScrollY(currentScrollY);
    };

    window.addEventListener('scroll', updateScrollDirection, { passive: true });
    
    return () => window.removeEventListener('scroll', updateScrollDirection);
  }, [lastScrollY]);

  return scrollDirection;
};
