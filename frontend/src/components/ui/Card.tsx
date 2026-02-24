import React from 'react';
import { clsx } from 'clsx';
import { motion } from 'framer-motion';
import { cardHover } from '../../utils/animations';
import { useReducedMotion } from '../../hooks/useReducedMotion';

interface CardProps extends Omit<React.HTMLAttributes<HTMLDivElement>, 'onDrag' | 'onDragStart' | 'onDragEnd'> {
  children: React.ReactNode;
  hoverable?: boolean; // Enable hover effects for clickable cards
}

export const Card: React.FC<CardProps> = ({ 
  className, 
  children, 
  hoverable = false,
  onClick,
  ...props 
}) => {
  const prefersReducedMotion = useReducedMotion();

  // Disable animations if reduced motion is preferred
  const hoverVariants = prefersReducedMotion ? undefined : cardHover;

  // Use motion.div for hoverable cards, regular div otherwise
  if (hoverable || onClick) {
    return (
      <motion.div
        className={clsx(
          'rounded-lg border bg-card text-card-foreground shadow-sm',
          'transition-colors duration-250',
          // Add will-change for frequently animated elements
          'will-change-transform',
          // Add cursor pointer for clickable cards
          onClick && 'cursor-pointer',
          className
        )}
        variants={hoverVariants}
        initial="rest"
        whileHover="hover"
        whileTap={onClick ? "active" : undefined}
        onClick={onClick}
        {...(props as any)}
      >
        {children}
      </motion.div>
    );
  }

  return (
    <div
      className={clsx(
        'rounded-lg border bg-card text-card-foreground shadow-sm',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

export const CardHeader: React.FC<CardProps> = ({ className, children, ...props }) => {
  return (
    <div className={clsx('flex flex-col space-y-2 p-6', className)} {...props}>
      {children}
    </div>
  );
};

export const CardTitle: React.FC<CardProps> = ({ className, children, ...props }) => {
  return (
    <h3
      className={clsx('text-2xl font-semibold leading-none tracking-tight', className)}
      {...props}
    >
      {children}
    </h3>
  );
};

export const CardDescription: React.FC<CardProps> = ({ className, children, ...props }) => {
  return (
    <p className={clsx('text-sm text-muted-foreground', className)} {...props}>
      {children}
    </p>
  );
};

export const CardContent: React.FC<CardProps> = ({ className, children, ...props }) => {
  return (
    <div className={clsx('p-6 pt-0', className)} {...props}>
      {children}
    </div>
  );
};

export const CardFooter: React.FC<CardProps> = ({ className, children, ...props }) => {
  return (
    <div className={clsx('flex items-center p-6 pt-0', className)} {...props}>
      {children}
    </div>
  );
};
