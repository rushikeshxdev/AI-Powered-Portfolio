import React from 'react';
import { motion } from 'framer-motion';
import { Award, Calendar, Building2 } from 'lucide-react';
import { resumeData } from '../data/resume';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';

export const Certifications: React.FC = () => {
  const { certifications } = resumeData;

  return (
    <section id="certifications" className="py-12 sm:py-16 md:py-20 bg-muted/30" aria-labelledby="certifications-heading">
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
          <h2 id="certifications-heading" className="text-3xl sm:text-4xl font-bold text-center mb-3 sm:mb-4">
            Certifications
          </h2>
          <p className="text-sm sm:text-base text-center text-muted-foreground mb-8 sm:mb-12 max-w-2xl mx-auto px-4">
            Professional certifications and specialized training in DevOps, cloud technologies, and security.
          </p>
        </motion.div>

        <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-6">
          {certifications.map((cert, index) => (
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
              <Card className="h-full hover:shadow-xl hover:shadow-primary/10 transition-all duration-300 border-2 hover:border-primary/30 group">
                <CardHeader>
                  <div className="flex items-start space-x-4">
                    <div className="p-3 rounded-lg bg-gradient-to-br from-primary/10 to-primary/5 group-hover:from-primary/20 group-hover:to-primary/10 transition-colors">
                      <Award className="h-8 w-8 text-primary" aria-hidden="true" />
                    </div>
                    <div className="flex-1">
                      <CardTitle className="text-xl mb-2">{cert.name}</CardTitle>
                      <div className="space-y-2 text-sm text-muted-foreground">
                        <div className="flex items-center">
                          <Building2 className="h-4 w-4 mr-2 text-primary" aria-hidden="true" />
                          <span className="font-medium">{cert.issuer}</span>
                        </div>
                        <div className="flex items-center">
                          <Calendar className="h-4 w-4 mr-2 text-primary" aria-hidden="true" />
                          <span>{cert.issued}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  {cert.description && (
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      {cert.description}
                    </p>
                  )}
                  
                  <div>
                    <h3 className="text-sm font-semibold mb-2 text-foreground">Skills Covered</h3>
                    <div className="flex flex-wrap gap-2">
                      {cert.skills.map((skill, skillIndex) => (
                        <span
                          key={skillIndex}
                          className="text-xs bg-secondary text-secondary-foreground px-3 py-1.5 rounded-full border border-border hover:border-primary hover:bg-primary/10 transition-all duration-200 cursor-default"
                        >
                          {skill}
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
    </section>
  );
};
