/**
 * Shared animation variants and configurations for Framer Motion
 * All animations use GPU-accelerated properties (transform, opacity)
 * for optimal performance
 */

import type { Variants } from 'framer-motion';

/**
 * Fade in with upward slide animation
 * Used for: subheadings, paragraphs, cards
 * Duration: 500ms (Requirements 2.2, 23.2)
 */
export const fadeInUp: Variants = {
  hidden: { 
    opacity: 0, 
    y: 30 
  },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: { 
      duration: 0.5, 
      ease: [0.25, 0.1, 0.25, 1] // cubic-bezier easing
    }
  }
};

/**
 * Container for staggered children animations
 * Used for: lists, grids, bullet points
 * Stagger delay: 100ms between children (Requirement 2.3)
 */
export const staggerContainer: Variants = {
  hidden: { 
    opacity: 0 
  },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1, // 100ms delay between items
      delayChildren: 0.2
    }
  }
};

/**
 * Scale animation on hover
 * Used for: buttons, cards, interactive elements
 * Scale range: 1.02-1.05 (Requirements 9.2, 25.1)
 * Duration: 200ms (Requirement 23.1)
 */
export const scaleOnHover: Variants = {
  rest: { 
    scale: 1 
  },
  hover: { 
    scale: 1.05,
    transition: { 
      duration: 0.2, 
      ease: [0.25, 0.1, 0.25, 1] // cubic-bezier easing (Requirement 10.3)
    }
  }
};

/**
 * Glow effect on hover
 * Used for: buttons, chatbot icon
 * Duration: 250ms (Requirement 10.2)
 */
export const glowOnHover: Variants = {
  rest: { 
    boxShadow: '0 0 0 rgba(var(--primary-rgb), 0)' 
  },
  hover: { 
    boxShadow: '0 0 20px rgba(var(--primary-rgb), 0.5)',
    transition: { 
      duration: 0.25,
      ease: [0.25, 0.1, 0.25, 1] // cubic-bezier easing
    }
  }
};

/**
 * Typing effect configuration
 * Used for: terminal component, hero heading
 */
export const typingConfig = {
  delayPerCharacter: 50,
  cursorBlinkSpeed: 530
};

/**
 * Scroll animation configuration
 * Trigger offset: 15% visibility (Requirement 11.2, 24)
 * Animate once per page load (Requirement 8.4, 16)
 */
export const scrollAnimationConfig = {
  triggerOffset: 0.15, // 15% visibility
  once: true // Animate only once
};

/**
 * Card-specific animation variants
 * Duration: 400ms (Requirement 8.1)
 * Stagger delay: 150ms (Requirement 8.2)
 */
export const cardVariants: Variants = {
  hidden: { 
    opacity: 0, 
    y: 20 
  },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: { 
      duration: 0.4,
      ease: [0.25, 0.1, 0.25, 1]
    }
  }
};

/**
 * Card container with stagger for multiple cards
 */
export const cardStaggerContainer: Variants = {
  hidden: { 
    opacity: 0 
  },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.15, // 150ms delay between cards
      delayChildren: 0.1
    }
  }
};

/**
 * Paragraph reveal animation
 * Duration: 400ms (Requirement 2.4)
 */
export const paragraphReveal: Variants = {
  hidden: { 
    opacity: 0, 
    y: 20 
  },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: { 
      duration: 0.4,
      ease: [0.25, 0.1, 0.25, 1]
    }
  }
};

/**
 * Section fade-in animation
 * Duration: 500ms (Requirement 11.1)
 */
export const sectionFadeIn: Variants = {
  hidden: { 
    opacity: 0 
  },
  visible: { 
    opacity: 1,
    transition: { 
      duration: 0.5,
      ease: [0.25, 0.1, 0.25, 1]
    }
  }
};

/**
 * Pulse animation for chatbot icon
 * Cycle duration: 2 seconds (Requirement 17.1)
 * Scale range: 1.0 to 1.15 (Requirement 17.2)
 */
export const pulseAnimation: Variants = {
  initial: { 
    scale: 1 
  },
  animate: {
    scale: [1, 1.15, 1],
    transition: {
      duration: 2,
      repeat: Infinity,
      ease: 'easeInOut'
    }
  }
};

/**
 * Button hover with scale and shadow
 * Scale: 1.05 (within 1.02-1.1 range)
 * Shadow increase: 4px+ blur radius (Requirement 9.3)
 */
export const buttonHover: Variants = {
  rest: { 
    scale: 1,
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)'
  },
  hover: { 
    scale: 1.05,
    boxShadow: '0 6px 12px rgba(0, 0, 0, 0.15)', // 4px+ increase in blur
    transition: { 
      duration: 0.2,
      ease: [0.25, 0.1, 0.25, 1]
    }
  }
};

/**
 * Card hover with border animation
 * Duration: 250ms (Requirement 10.2)
 */
export const cardHover: Variants = {
  rest: { 
    scale: 1,
    borderColor: 'rgba(var(--border-rgb), 0.2)'
  },
  hover: { 
    scale: 1.02,
    borderColor: 'rgba(var(--primary-rgb), 0.5)',
    transition: { 
      duration: 0.25,
      ease: [0.25, 0.1, 0.25, 1]
    }
  }
};

/**
 * Active state animation for interactive elements
 * Used for: click feedback (Requirement 24.5)
 */
export const activeState: Variants = {
  rest: { 
    scale: 1 
  },
  active: { 
    scale: 0.95,
    transition: { 
      duration: 0.1,
      ease: 'easeOut'
    }
  }
};
