import React from 'react';
import { clsx } from 'clsx';
import { motion } from 'framer-motion';
import { buttonHover } from '../../utils/animations';
import { useReducedMotion } from '../../hooks/useReducedMotion';

interface ButtonProps extends Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, 'onDrag' | 'onDragStart' | 'onDragEnd'> {
  variant?: 'default' | 'outline' | 'ghost';
  size?: 'default' | 'sm' | 'lg';
  loading?: boolean;
  success?: boolean;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'default',
  size = 'default',
  loading = false,
  success = false,
  className,
  children,
  disabled,
  ...props
}) => {
  const prefersReducedMotion = useReducedMotion();

  const baseClasses = clsx(
    'inline-flex items-center justify-center rounded-md font-medium',
    'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
    'disabled:opacity-50 disabled:pointer-events-none',
    'transition-colors duration-200',
    {
      'bg-primary text-primary-foreground hover:bg-primary/90': variant === 'default',
      'border border-input bg-background hover:bg-accent hover:text-accent-foreground': variant === 'outline',
      'hover:bg-accent hover:text-accent-foreground': variant === 'ghost',
      'h-10 py-2 px-4': size === 'default',
      'h-9 px-3 text-sm': size === 'sm',
      'h-11 px-8': size === 'lg',
    },
    className
  );

  const buttonStyle = {
    boxShadow: variant === 'default' 
      ? '0 2px 4px rgba(0, 0, 0, 0.1)' 
      : '0 1px 2px rgba(0, 0, 0, 0.05)',
  };

  // If reduced motion is preferred, use regular button
  if (prefersReducedMotion) {
    return (
      <button
        className={baseClasses}
        disabled={disabled || loading}
        style={buttonStyle}
        {...props}
      >
        {loading && (
          <svg
            className="mr-2 h-4 w-4 animate-spin"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        )}
        {success && (
          <svg
            className="mr-2 h-4 w-4"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M5 13l4 4L19 7"
            />
          </svg>
        )}
        {children}
      </button>
    );
  }

  // Use motion.button with animations
  return (
    <motion.button
      className={clsx(baseClasses, 'will-change-transform')}
      variants={buttonHover}
      initial="rest"
      whileHover={disabled || loading ? undefined : "hover"}
      whileTap={disabled || loading ? undefined : "active"}
      disabled={disabled || loading}
      style={buttonStyle}
      {...(props as any)}
    >
      {loading && (
        <motion.svg
          className="mr-2 h-4 w-4 animate-spin"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.2 }}
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </motion.svg>
      )}
      {success && (
        <motion.svg
          className="mr-2 h-4 w-4"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          initial={{ scale: 0, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.3, ease: 'easeOut' }}
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M5 13l4 4L19 7"
          />
        </motion.svg>
      )}
      {children}
    </motion.button>
  );
};
