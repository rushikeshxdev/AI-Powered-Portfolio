import React from 'react';
import { motion } from 'framer-motion';
import { GraduationCap, Calendar, MapPin, BookOpen } from 'lucide-react';
import { resumeData } from '../data/resume';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';

export const Education: React.FC = () => {
  const { education } = resumeData;

  return (
    <section id="education" className="py-12 sm:py-16 md:py-20 bg-background" aria-labelledby="education-heading">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.15 }}
          transition={{
            type: "spring",
            stiffness: 100,
            damping: 15,
          }}
        >
          <h2 id="education-heading" className="text-3xl sm:text-4xl font-bold text-center mb-3 sm:mb-4">
            Education
          </h2>
          <p className="text-sm sm:text-base text-center text-muted-foreground mb-8 sm:mb-12 max-w-2xl mx-auto px-4">
            Academic background and relevant coursework in computer science and software engineering.
          </p>
        </motion.div>

        <div className="max-w-4xl mx-auto space-y-6">
          {education.map((entry, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.15 }}
              transition={{
                type: "spring",
                stiffness: 100,
                damping: 15,
                delay: 0.1 * index,
              }}
            >
              <Card className="hover:shadow-xl hover:shadow-primary/10 transition-all duration-300 border-2 hover:border-primary/30 group">
                <CardHeader>
                  <div className="flex items-start space-x-4">
                    <div className="p-3 rounded-lg bg-gradient-to-br from-primary/10 to-primary/5 group-hover:from-primary/20 group-hover:to-primary/10 transition-colors">
                      <GraduationCap className="h-8 w-8 text-primary" aria-hidden="true" />
                    </div>
                    <div className="flex-1">
                      <CardTitle className="text-2xl mb-2">{entry.institution}</CardTitle>
                      <p className="text-lg text-foreground font-semibold">{entry.qualification}</p>
                    </div>
                    <div className="text-right">
                      <div className="inline-flex items-center px-4 py-2 rounded-full bg-primary/10 border border-primary/20">
                        <span className="text-xl font-bold text-primary">{entry.score}</span>
                      </div>
                      <p className="text-xs text-muted-foreground mt-1">
                        {entry.score.includes('CGPA') ? 'CGPA' : 'Score'}
                      </p>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                    <div className="flex items-center">
                      <Calendar className="h-4 w-4 mr-2 text-primary" aria-hidden="true" />
                      <span>{entry.year}</span>
                    </div>
                    <div className="flex items-center">
                      <MapPin className="h-4 w-4 mr-2 text-primary" aria-hidden="true" />
                      <span>India</span>
                    </div>
                  </div>

                  {entry.relevant_coursework && entry.relevant_coursework.length > 0 && (
                    <div>
                      <div className="flex items-center mb-3">
                        <BookOpen className="h-5 w-5 mr-2 text-primary" aria-hidden="true" />
                        <h3 className="text-lg font-semibold">Relevant Coursework</h3>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {entry.relevant_coursework.map((course, courseIndex) => (
                          <span
                            key={courseIndex}
                            className="text-sm bg-secondary text-secondary-foreground px-3 py-1.5 rounded-full border border-border hover:border-primary hover:bg-primary/10 transition-all duration-200 cursor-default"
                          >
                            {course}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};
