import React from 'react';
import { Card } from './ui/Card';
import { motion } from 'framer-motion';
import { useReducedMotion } from '../hooks/useReducedMotion';

interface SkillCardProps {
  title: string;
  description: string;
  icon?: React.ReactNode;
  className?: string;
}

export const SkillCard: React.FC<SkillCardProps> = ({
  title,
  description,
  icon,
  className = '',
}) => {
  const prefersReducedMotion = useReducedMotion();

  const cardContent = (
    <div className="p-6">
      {/* Title with optional icon */}
      <div className="flex items-center gap-3 mb-3">
        {icon && (
          <div className="text-primary flex-shrink-0">
            {icon}
          </div>
        )}
        <h3 className="text-xl font-semibold text-foreground">
          {title}
        </h3>
      </div>

      {/* Multi-line description */}
      <p className="text-sm text-muted-foreground leading-relaxed">
        {description}
      </p>
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
