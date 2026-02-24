/**
 * Hook to detect user's prefers-reduced-motion preference
 * Respects accessibility requirements (Requirement 21.1, 21.4)
 * 
 * When reduced motion is enabled:
 * - Decorative animations are disabled (Requirement 21.2)
 * - Essential animations are reduced to max 100ms (Requirement 21.2)
 * - Parallax and particle effects are disabled (Requirement 21.3)
 */

import { useEffect, useState } from 'react';

export const useReducedMotion = (): boolean => {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  useEffect(() => {
    // Check if matchMedia is supported
    if (typeof window === 'undefined' || !window.matchMedia) {
      return;
    }

    // Query the prefers-reduced-motion media query
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    
    // Set initial value
    setPrefersReducedMotion(mediaQuery.matches);

    // Listen for changes to the preference
    const handleChange = (event: MediaQueryListEvent) => {
      setPrefersReducedMotion(event.matches);
    };

    // Add event listener (supports both modern and legacy APIs)
    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener('change', handleChange);
    } else {
      // Fallback for older browsers
      mediaQuery.addListener(handleChange);
    }

    // Cleanup
    return () => {
      if (mediaQuery.removeEventListener) {
        mediaQuery.removeEventListener('change', handleChange);
      } else {
        // Fallback for older browsers
        mediaQuery.removeListener(handleChange);
      }
    };
  }, []);

  return prefersReducedMotion;
};

/**
 * Get animation duration based on reduced motion preference
 * Essential animations: max 100ms when reduced motion enabled
 * Decorative animations: 0ms when reduced motion enabled
 */
export const getAnimationDuration = (
  normalDuration: number,
  isEssential: boolean = false,
  prefersReducedMotion: boolean = false
): number => {
  if (!prefersReducedMotion) {
    return normalDuration;
  }

  if (isEssential) {
    // Essential animations reduced to max 100ms
    return Math.min(normalDuration, 100);
  }

  // Decorative animations disabled
  return 0;
};

/**
 * Check if animation should be enabled based on reduced motion preference
 * Decorative animations disabled when reduced motion enabled
 */
export const shouldAnimate = (
  isEssential: boolean = false,
  prefersReducedMotion: boolean = false
): boolean => {
  if (!prefersReducedMotion) {
    return true;
  }

  // Only essential animations allowed when reduced motion enabled
  return isEssential;
};
