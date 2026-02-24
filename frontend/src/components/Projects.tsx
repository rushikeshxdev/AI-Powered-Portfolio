import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { resumeData } from '../data/resume';
import { ProjectCard } from './ProjectCard';

type FilterType = 'ALL' | 'AI/ML' | 'FULL STACK' | 'TYPESCRIPT';

export const Projects: React.FC = () => {
  const { projects } = resumeData;
  const [activeFilter, setActiveFilter] = useState<FilterType>('ALL');

  const filters: FilterType[] = ['ALL', 'AI/ML', 'FULL STACK', 'TYPESCRIPT'];

  const filterProjects = () => {
    if (activeFilter === 'ALL') return projects;
    
    return projects.filter(project => {
      const techs = project.technologies.join(' ').toLowerCase();
      const skills = project.skills_demonstrated?.join(' ').toLowerCase() || '';
      
      switch (activeFilter) {
        case 'AI/ML':
          return techs.includes('ai') || techs.includes('gemini') || skills.includes('ai') || skills.includes('ml');
        case 'FULL STACK':
          return (techs.includes('react') || techs.includes('node') || techs.includes('express')) && 
                 (techs.includes('mongodb') || techs.includes('postgresql'));
        case 'TYPESCRIPT':
          return techs.includes('typescript');
        default:
          return true;
      }
    });
  };

  const filteredProjects = filterProjects();

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  return (
    <section id="projects" className="py-12 sm:py-16 md:py-20 relative overflow-hidden" aria-labelledby="projects-heading">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-background to-primary/10" aria-hidden="true" />
      
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.15 }}
          transition={{ 
            type: "spring",
            stiffness: 100,
            damping: 15
          }}
        >
          <h2 id="projects-heading" className="text-3xl sm:text-4xl font-bold text-center mb-4 sm:mb-6">
            Open Source Projects
          </h2>
          <p className="text-sm sm:text-base text-center text-muted-foreground mb-8 max-w-2xl mx-auto px-4 leading-relaxed">
            A showcase of my recent work, featuring full-stack applications, AI integrations,
            and innovative solutions to real-world problems.
          </p>

          {/* Filter Buttons */}
          <div className="flex flex-wrap justify-center gap-4 mb-10">
            {filters.map((filter) => (
              <button
                key={filter}
                onClick={() => setActiveFilter(filter)}
                className={`px-4 py-2 rounded-full text-sm font-medium font-mono transition-all duration-300 ${
                  activeFilter === filter
                    ? 'bg-primary text-primary-foreground shadow-glow'
                    : 'bg-secondary text-secondary-foreground hover:bg-primary/20 border border-border'
                }`}
                aria-label={`Filter projects by ${filter}`}
                aria-pressed={activeFilter === filter}
              >
                {filter}
              </button>
            ))}
          </div>
        </motion.div>

        <motion.div
          key={activeFilter}
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-2 gap-6 sm:gap-8 max-w-7xl mx-auto"
        >
          {filteredProjects.map((project, index) => (
            <ProjectCard key={index} project={project} index={index} />
          ))}
        </motion.div>

        {filteredProjects.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12"
          >
            <p className="text-muted-foreground text-lg">
              No projects found for this filter.
            </p>
          </motion.div>
        )}
      </div>
    </section>
  );
};
