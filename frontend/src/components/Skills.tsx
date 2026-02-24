import React from 'react';
import { motion } from 'framer-motion';
import { Code, Layout, Server, Database, Cloud, Brain } from 'lucide-react';
import { resumeData } from '../data/resume';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';

export const Skills: React.FC = () => {
  const { skills } = resumeData;

  const skillCategories = [
    {
      title: 'Frontend & UI',
      icon: Layout,
      skills: skills.frontend,
      color: 'text-green-500',
    },
    {
      title: 'Backend Architecture',
      icon: Server,
      skills: skills.backend,
      color: 'text-blue-500',
    },
    {
      title: 'Agentic AI & ML',
      icon: Brain,
      skills: skills.ai_ml,
      color: 'text-purple-500',
    },
    {
      title: 'Languages',
      icon: Code,
      skills: skills.languages,
      color: 'text-orange-500',
    },
    {
      title: 'Database & Cloud',
      icon: Database,
      skills: skills.databases,
      color: 'text-cyan-500',
    },
    {
      title: 'DevOps & Tools',
      icon: Cloud,
      skills: skills.devops,
      color: 'text-pink-500',
    },
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.12,
        delayChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, scale: 0.8, y: 20 },
    visible: {
      opacity: 1,
      scale: 1,
      y: 0,
      transition: { 
        type: "spring" as const,
        stiffness: 150,
        damping: 12
      },
    },
  };

  const badgeContainerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.04,
        delayChildren: 0.2,
      },
    },
  };

  const badgeVariants = {
    hidden: { opacity: 0, scale: 0, rotate: -10 },
    visible: {
      opacity: 1,
      scale: 1,
      rotate: 0,
      transition: {
        type: "spring" as const,
        stiffness: 200,
        damping: 15,
      },
    },
  };

  return (
    <section id="skills" className="py-12 sm:py-16 md:py-20 bg-background" aria-labelledby="skills-heading">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
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
          <h2 id="skills-heading" className="text-3xl sm:text-4xl font-bold text-center mb-4 sm:mb-6">
            Technical Arsenal
          </h2>
          <p className="text-sm sm:text-base text-center text-muted-foreground mb-8 sm:mb-12 max-w-2xl mx-auto px-4">
            A comprehensive toolkit spanning full-stack development, AI/ML, and modern DevOps practices.
          </p>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.15 }}
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 max-w-7xl mx-auto"
        >
          {skillCategories.map((category, index) => {
            const Icon = category.icon;
            return (
              <motion.div key={index} variants={itemVariants}>
                <Card className="h-full hover:shadow-xl hover:shadow-primary/10 transition-all duration-300 border-2 hover:border-primary/30 group">
                  <CardHeader>
                    <div className="flex items-center">
                      <div className="p-2 rounded-lg bg-gradient-to-br from-primary/10 to-primary/5 mr-3 group-hover:from-primary/20 group-hover:to-primary/10 transition-colors">
                        <Icon className={`h-5 w-5 sm:h-6 sm:w-6 ${category.color}`} aria-hidden="true" />
                      </div>
                      <CardTitle className="text-lg sm:text-xl">{category.title}</CardTitle>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <motion.div 
                      className="flex flex-wrap gap-2"
                      variants={badgeContainerVariants}
                      initial="hidden"
                      whileInView="visible"
                      viewport={{ once: true, amount: 0.15 }}
                      role="list"
                      aria-label={`${category.title} skills`}
                    >
                      {category.skills.map((skill, idx) => (
                        <motion.span
                          key={idx}
                          role="listitem"
                          variants={badgeVariants}
                          whileHover={{ 
                            scale: 1.1,
                            y: -2,
                            transition: { 
                              type: "spring",
                              stiffness: 400,
                              damping: 10
                            }
                          }}
                          className="text-xs sm:text-sm bg-secondary text-secondary-foreground px-3 py-1.5 rounded-full hover:bg-primary hover:text-primary-foreground transition-all duration-200 cursor-default border border-border hover:border-primary font-medium"
                        >
                          {skill}
                        </motion.span>
                      ))}
                    </motion.div>
                  </CardContent>
                </Card>
              </motion.div>
            );
          })}
        </motion.div>
      </div>
    </section>
  );
};
