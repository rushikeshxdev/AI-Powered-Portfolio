import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Github, ExternalLink } from 'lucide-react';
import type { ProjectCardProps } from '../types';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/Card';
import { Button } from './ui/Button';
import { Skeleton } from './ui/Skeleton';

export const ProjectCard: React.FC<ProjectCardProps> = ({ project, index }) => {
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);

  const cardVariants = {
    hidden: { 
      opacity: 0, 
      x: index % 2 === 0 ? -50 : 50,
      y: 30
    },
    visible: {
      opacity: 1,
      x: 0,
      y: 0,
      transition: {
        type: "spring" as const,
        stiffness: 100,
        damping: 15,
        delay: index * 0.15,
      },
    },
  };

  // Helper function to get tech badge color
  const getTechBadgeClass = (tech: string): string => {
    const techLower = tech.toLowerCase();
    if (techLower.includes('react') || techLower.includes('redux')) return 'tech-badge-react';
    if (techLower.includes('typescript') || techLower.includes('javascript')) return 'tech-badge-typescript';
    if (techLower.includes('python') || techLower.includes('fastapi')) return 'tech-badge-python';
    if (techLower.includes('node') || techLower.includes('express')) return 'tech-badge-node';
    if (techLower.includes('ai') || techLower.includes('gemini') || techLower.includes('openrouter')) return 'tech-badge-ai';
    return 'tech-badge-default';
  };

  return (
    <motion.div
      variants={cardVariants}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: "-50px" }}
      whileHover={{ 
        y: -16, 
        transition: { 
          type: "spring",
          stiffness: 300,
          damping: 20
        } 
      }}
      className="group"
    >
      <Card className="h-full flex flex-col hover:shadow-3xl hover:shadow-primary/30 transition-all duration-300 border-2 hover:border-primary hover:shadow-glow overflow-hidden">
        <CardHeader className="pb-3">
          <CardTitle className="text-xl sm:text-2xl group-hover:text-primary transition-colors">
            {project.name}
          </CardTitle>
          {project.subtitle && (
            <CardDescription className="text-sm sm:text-base font-semibold text-primary/80 group-hover:text-primary transition-colors">
              {project.subtitle}
            </CardDescription>
          )}
        </CardHeader>
        
        {/* Lazy-loaded project image with loading skeleton */}
        {project.imageUrl && !imageError && (
          <div className="relative w-full h-48 overflow-hidden">
            {!imageLoaded && (
              <Skeleton className="absolute inset-0 w-full h-full" />
            )}
            <img
              src={project.imageUrl}
              alt={`${project.name} preview`}
              loading="lazy"
              className={`w-full h-full object-cover transition-all duration-500 group-hover:scale-115 ${
                imageLoaded ? 'opacity-100' : 'opacity-0'
              }`}
              onLoad={() => setImageLoaded(true)}
              onError={() => setImageError(true)}
            />
          </div>
        )}
        
        <CardContent className="flex-1 flex flex-col pt-4">
          <p className="text-sm sm:text-base text-muted-foreground mb-5 line-clamp-3 leading-relaxed">
            {project.description}
          </p>

          {/* Technologies */}
          <div className="mb-5">
            <p className="text-xs sm:text-sm font-bold mb-2.5 text-foreground">Technologies</p>
            <div className="flex flex-wrap gap-2" role="list" aria-label={`Technologies used in ${project.name}`}>
              {project.technologies.map((tech, idx) => (
                <span
                  key={idx}
                  role="listitem"
                  className={`text-xs font-medium px-3 py-1.5 rounded-full transition-all duration-200 hover:scale-105 ${getTechBadgeClass(tech)}`}
                >
                  {tech}
                </span>
              ))}
            </div>
          </div>

          {/* Highlights */}
          {project.highlights && project.highlights.length > 0 && (
            <div className="mb-5">
              <p className="text-xs sm:text-sm font-bold mb-2.5 text-foreground">Key Highlights</p>
              <ul className="space-y-2" aria-label={`Key highlights of ${project.name}`}>
                {project.highlights.slice(0, 2).map((highlight, idx) => (
                  <li key={idx} className="text-xs sm:text-sm text-muted-foreground flex items-start leading-relaxed">
                    <span className="text-primary mr-2 mt-0.5 font-bold" aria-hidden="true">✓</span>
                    <span className="line-clamp-2">{highlight}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Links */}
          <div className="mt-auto pt-4 flex flex-col sm:flex-row gap-4">
            {project.github && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => window.open(project.github, '_blank', 'noopener,noreferrer')}
                className="flex items-center justify-center w-full sm:w-auto border-2 hover:border-primary hover:bg-primary/10 transition-all duration-200 hover:scale-108 hover:shadow-md hover:shadow-primary/20 shimmer-button"
                aria-label={`View ${project.name} source code on GitHub (opens in new tab)`}
              >
                <Github className="h-4 w-4 mr-2" aria-hidden="true" />
                GitHub
              </Button>
            )}
            {project.demo && (
              <Button
                variant="default"
                size="sm"
                onClick={() => window.open(project.demo, '_blank', 'noopener,noreferrer')}
                className="flex items-center justify-center w-full sm:w-auto shadow-md hover:shadow-xl hover:shadow-primary/40 transition-all duration-200 hover:scale-108 shimmer-button"
                aria-label={`View ${project.name} live demo (opens in new tab)`}
              >
                <ExternalLink className="h-4 w-4 mr-2" aria-hidden="true" />
                Demo
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};
