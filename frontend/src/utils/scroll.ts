/**
 * Smooth scroll utility with timing control and reduced motion support
 * Validates: Requirements 10.1, 10.2, 10.3
 */

/**
 * Smoothly scrolls to a target element with animation
 * 
 * @param targetId - The ID of the target element (without #)
 * @param duration - Animation duration in milliseconds (default: 800ms)
 * @returns Promise that resolves when scroll completes or rejects if target not found
 * 
 * Features:
 * - 800ms scroll animation duration (Requirement 10.2)
 * - Instant scroll when reduced motion is enabled (Requirement 10.3)
 * - Graceful error handling for missing targets
 * - Smooth easing function for natural feel
 */
export const smoothScrollTo = (
  targetId: string,
  duration: number = 800
): Promise<void> => {
  return new Promise((resolve, reject) => {
    // Find the target element
    const targetElement = document.getElementById(targetId);
    
    if (!targetElement) {
      console.warn(`Scroll target not found: #${targetId}`);
      reject(new Error(`Target element #${targetId} not found`));
      return;
    }

    // Check for reduced motion preference
    const prefersReducedMotion = window.matchMedia(
      '(prefers-reduced-motion: reduce)'
    ).matches;

    // If reduced motion is enabled, perform instant scroll
    if (prefersReducedMotion) {
      targetElement.scrollIntoView({ behavior: 'auto', block: 'start' });
      resolve();
      return;
    }

    // Get starting position
    const startPosition = window.pageYOffset;
    const targetPosition = targetElement.getBoundingClientRect().top + startPosition;
    const distance = targetPosition - startPosition;
    
    // If already at target, resolve immediately
    if (Math.abs(distance) < 1) {
      resolve();
      return;
    }

    let startTime: number | null = null;

    // Easing function for smooth animation (ease-in-out)
    const easeInOutCubic = (t: number): number => {
      return t < 0.5
        ? 4 * t * t * t
        : 1 - Math.pow(-2 * t + 2, 3) / 2;
    };

    // Animation function
    const animation = (currentTime: number) => {
      if (startTime === null) {
        startTime = currentTime;
      }

      const timeElapsed = currentTime - startTime;
      const progress = Math.min(timeElapsed / duration, 1);
      const ease = easeInOutCubic(progress);

      window.scrollTo(0, startPosition + distance * ease);

      if (progress < 1) {
        requestAnimationFrame(animation);
      } else {
        resolve();
      }
    };

    // Start the animation
    requestAnimationFrame(animation);
  });
};

/**
 * Scrolls to a target element by ID with error handling
 * Convenience wrapper around smoothScrollTo
 * 
 * @param targetId - The ID of the target element (with or without #)
 * @param duration - Animation duration in milliseconds (default: 800ms)
 */
export const scrollToElement = async (
  targetId: string,
  duration?: number
): Promise<void> => {
  // Remove # if present
  const cleanId = targetId.startsWith('#') ? targetId.slice(1) : targetId;
  
  try {
    await smoothScrollTo(cleanId, duration);
  } catch (error) {
    // Error already logged in smoothScrollTo
    // Fail silently to not disrupt user experience
  }
};

/**
 * Scrolls to the top of the page
 * 
 * @param duration - Animation duration in milliseconds (default: 800ms)
 */
export const scrollToTop = (duration: number = 800): Promise<void> => {
  return new Promise((resolve) => {
    // Check for reduced motion preference
    const prefersReducedMotion = window.matchMedia(
      '(prefers-reduced-motion: reduce)'
    ).matches;

    // If reduced motion is enabled, perform instant scroll
    if (prefersReducedMotion) {
      window.scrollTo({ top: 0, behavior: 'auto' });
      resolve();
      return;
    }

    const startPosition = window.pageYOffset;
    
    if (startPosition === 0) {
      resolve();
      return;
    }

    let startTime: number | null = null;

    const easeInOutCubic = (t: number): number => {
      return t < 0.5
        ? 4 * t * t * t
        : 1 - Math.pow(-2 * t + 2, 3) / 2;
    };

    const animation = (currentTime: number) => {
      if (startTime === null) {
        startTime = currentTime;
      }

      const timeElapsed = currentTime - startTime;
      const progress = Math.min(timeElapsed / duration, 1);
      const ease = easeInOutCubic(progress);

      window.scrollTo(0, startPosition * (1 - ease));

      if (progress < 1) {
        requestAnimationFrame(animation);
      } else {
        resolve();
      }
    };

    requestAnimationFrame(animation);
  });
};
