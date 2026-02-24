import React from 'react';
import { Card } from './ui/Card';
import { motion } from 'framer-motion';
import { useReducedMotion } from '../hooks/useReducedMotion';

interface MetricCardProps {
  value: string;
  label: string;
  description: string;
  icon?: React.ReactNode;
  className?: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  value,
  label,
  description,
  icon,
  className = '',
}) => {
  const prefersReducedMotion = useReducedMotion();

  const cardContent = (
    <div className="relative p-6">
      {/* Optional icon in top-right corner */}
      {icon && (
        <div className="absolute top-4 right-4 text-primary/60">
          {icon}
        </div>
      )}

      {/* Large value text */}
      <div className="text-3xl font-bold text-primary mb-2">
        {value}
      </div>

      {/* Label text */}
      <div className="text-lg font-semibold text-foreground mb-1">
        {label}
      </div>

      {/* Description text */}
      <div className="text-sm text-muted-foreground">
        {description}
      </div>
    </div>
  );

  // Wrap in motion.div for hover effects if animations are enabled
  if (!prefersReducedMotion) {
    return (
      <motion.div
        className={className}
        whileHover={{ scale: 1.02 }}
        transition={{ duration: 0.2 }}
      >
        <Card className="h-full border-border hover:border-primary/50 transition-colors duration-200">
          {cardContent}
        </Card>
      </motion.div>
    );
  }

  // Static card for reduced motion
  return (
    <div className={className}>
      <Card className="h-full border-border">
        {cardContent}
      </Card>
    </div>
  );
};
