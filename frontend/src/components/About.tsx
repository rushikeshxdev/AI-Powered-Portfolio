import React from 'react';
import { motion } from 'framer-motion';
import { Briefcase } from 'lucide-react';
import { resumeData } from '../data/resume';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { cardStaggerContainer, cardVariants } from '../utils/animations';
import { useReducedMotion } from '../hooks/useReducedMotion';

export const About: React.FC = () => {
  const { experience } = resumeData;
  const prefersReducedMotion = useReducedMotion();

  return (
    <section id="experience" className="py-12 sm:py-16 md:py-20 bg-background" aria-labelledby="experience-heading">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.15 }}
          variants={prefersReducedMotion ? undefined : cardStaggerContainer}
        >
          {/* Experience Section */}
          <div>
            <h2 id="experience-heading" className="text-3xl sm:text-4xl font-bold mb-8 text-center flex items-center justify-center">
              <Briefcase className="h-8 w-8 text-primary mr-3" aria-hidden="true" />
              Experience
            </h2>
            <div className="max-w-4xl mx-auto">
              {experience.map((exp, index) => (
                <motion.div
                  key={index}
                  variants={prefersReducedMotion ? undefined : cardVariants}
                >
                  <Card className="h-full hover:shadow-xl hover:shadow-primary/10 transition-all duration-300 border-2 hover:border-primary/50 hover:scale-[1.05]">
                    <CardHeader>
                      <CardTitle className="text-xl sm:text-2xl">{exp.role}</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-sm sm:text-base text-primary font-semibold mb-2">{exp.company}</p>
                      <p className="text-sm sm:text-base text-muted-foreground mb-4">
                        {exp.duration} • {exp.location}
                      </p>
                      
                      <div className="mt-4">
                        <p className="text-sm sm:text-base font-bold mb-4">Key Responsibilities</p>
                        <ul className="space-y-2" aria-label="Key responsibilities">
                          {exp.responsibilities.map((resp, respIndex) => (
                            <li key={respIndex} className="text-xs sm:text-sm text-muted-foreground flex items-start leading-relaxed">
                              <span className="text-primary mr-2 font-bold" aria-hidden="true">✓</span>
                              <span>{resp}</span>
                            </li>
                          ))}
                        </ul>
                      </div>

                      <div className="mt-4">
                        <p className="text-sm sm:text-base font-bold mb-4">Technologies</p>
                        <div className="flex flex-wrap gap-2" role="list" aria-label="Technologies used">
                          {exp.technologies.map((tech, techIndex) => (
                            <span
                              key={techIndex}
                              role="listitem"
                              className="text-xs bg-primary/10 text-primary px-3 py-1.5 rounded-full border border-primary/20 font-medium"
                            >
                              {tech}
                            </span>
                          ))}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};
