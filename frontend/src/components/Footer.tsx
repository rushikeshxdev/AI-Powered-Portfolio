import React from 'react';
import { Github, Linkedin, Mail, Download, Heart } from 'lucide-react';
import { motion } from 'framer-motion';
import { resumeData } from '../data/resume';
import { Button } from './ui/Button';
import { useReducedMotion } from '../hooks/useReducedMotion';

export const Footer: React.FC = () => {
  const { personal } = resumeData;
  const prefersReducedMotion = useReducedMotion();

  // If reduced motion is preferred, use regular elements
  if (prefersReducedMotion) {
    return (
      <footer className="bg-card border-t border-border py-12 sm:py-16" role="contentinfo">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          {/* CTA Section - Enhanced with glassmorphism */}
          <div className="relative mb-16 overflow-hidden">
            {/* Background decorative elements */}
            <div className="absolute inset-0 bg-gradient-to-br from-purple-500/10 via-transparent to-emerald-500/10 rounded-3xl" />
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_50%,rgba(107,70,193,0.1),transparent_50%)]" />
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_50%,rgba(16,185,129,0.1),transparent_50%)]" />
            
            {/* Glassmorphic card */}
            <div className="relative backdrop-blur-xl bg-gradient-to-br from-card/80 via-card/60 to-card/80 border border-primary/20 rounded-3xl p-8 sm:p-12 shadow-2xl">
              {/* Subtle border glow */}
              <div className="absolute inset-0 rounded-3xl bg-gradient-to-br from-purple-500/20 via-transparent to-emerald-500/20 opacity-50" />
              
              <div className="relative text-center">
                <h3 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-purple-400 via-purple-600 to-emerald-500 bg-clip-text text-transparent leading-tight">
                  Let's build something together
                </h3>
                <p className="text-muted-foreground text-base sm:text-lg mb-8 max-w-2xl mx-auto leading-relaxed">
                  I'm always interested in hearing about new projects and opportunities. Let's create something amazing!
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <Button
                    size="lg"
                    onClick={() => window.location.href = `mailto:${personal.email}`}
                    className="shadow-glow hover:shadow-glow-lg transition-all duration-300 text-base sm:text-lg px-8 py-6 bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-500 hover:to-purple-600"
                  >
                    <Mail className="h-5 w-5 mr-2" aria-hidden="true" />
                    Get in Touch
                  </Button>
                  <Button
                    size="lg"
                    variant="outline"
                    onClick={() => window.open('/resume.pdf', '_blank', 'noopener,noreferrer')}
                    className="border-2 border-primary/50 hover:border-primary text-base sm:text-lg px-8 py-6 hover:bg-primary/10 backdrop-blur-sm"
                  >
                    <Download className="h-5 w-5 mr-2" aria-hidden="true" />
                    Download Resume
                  </Button>
                </div>
              </div>
            </div>
          </div>

          {/* Divider */}
          <div className="border-t border-border mb-8" />

          {/* Footer Content */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
            {/* About */}
            <div>
              <h4 className="text-lg font-bold font-mono text-primary mb-4">&lt;RR /&gt;</h4>
              <p className="text-sm text-muted-foreground">
                Full Stack Developer specializing in AI-powered applications and modern web technologies.
              </p>
            </div>

            {/* Quick Links */}
            <div>
              <h4 className="text-sm font-semibold mb-4 text-foreground">Quick Links</h4>
              <div className="space-y-2 text-sm">
                <button
                  onClick={() => document.getElementById('experience')?.scrollIntoView({ behavior: 'smooth' })}
                  className="block text-muted-foreground hover:text-primary transition-colors"
                >
                  Experience
                </button>
                <button
                  onClick={() => document.getElementById('projects')?.scrollIntoView({ behavior: 'smooth' })}
                  className="block text-muted-foreground hover:text-primary transition-colors"
                >
                  Projects
                </button>
                <button
                  onClick={() => document.getElementById('skills')?.scrollIntoView({ behavior: 'smooth' })}
                  className="block text-muted-foreground hover:text-primary transition-colors"
                >
                  Skills
                </button>
              </div>
            </div>

            {/* Connect */}
            <div>
              <h4 className="text-sm font-semibold mb-4 text-foreground">Connect</h4>
              <div className="flex space-x-4 mb-4" role="list" aria-label="Social media links">
                <a
                  href={personal.github}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-muted-foreground hover:text-primary transition-colors p-2 hover:bg-primary/10 rounded-lg"
                  aria-label="Visit GitHub profile (opens in new tab)"
                  role="listitem"
                >
                  <Github className="h-5 w-5" aria-hidden="true" />
                </a>
                <a
                  href={personal.linkedin}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-muted-foreground hover:text-primary transition-colors p-2 hover:bg-primary/10 rounded-lg"
                  aria-label="Visit LinkedIn profile (opens in new tab)"
                  role="listitem"
                >
                  <Linkedin className="h-5 w-5" aria-hidden="true" />
                </a>
                <a
                  href={`mailto:${personal.email}`}
                  className="text-muted-foreground hover:text-primary transition-colors p-2 hover:bg-primary/10 rounded-lg"
                  aria-label={`Send email to ${personal.email}`}
                  role="listitem"
                >
                  <Mail className="h-5 w-5" aria-hidden="true" />
                </a>
              </div>
              <p className="text-sm text-muted-foreground">
                {personal.email}
              </p>
            </div>
          </div>

          {/* Copyright */}
          <div className="text-center pt-8 border-t border-border">
            <p className="text-sm text-muted-foreground flex items-center justify-center gap-2">
              © {new Date().getFullYear()} {personal.name}. Built with
              <Heart className="h-4 w-4 text-primary fill-primary" aria-hidden="true" />
              using React, TypeScript & FastAPI
            </p>
          </div>
        </div>
      </footer>
    );
  }

  return (
    <footer className="bg-card border-t border-border py-12 sm:py-16" role="contentinfo">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        {/* CTA Section - Enhanced with glassmorphism and animations */}
        <motion.div 
          className="relative mb-16 overflow-hidden"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          {/* Animated background decorative elements */}
          <motion.div 
            className="absolute inset-0 bg-gradient-to-br from-purple-500/10 via-transparent to-emerald-500/10 rounded-3xl"
            animate={{ 
              backgroundPosition: ['0% 0%', '100% 100%'],
            }}
            transition={{ 
              duration: 10, 
              repeat: Infinity, 
              repeatType: 'reverse' 
            }}
          />
          <motion.div 
            className="absolute inset-0 bg-[radial-gradient(circle_at_30%_50%,rgba(107,70,193,0.15),transparent_50%)]"
            animate={{ 
              opacity: [0.3, 0.6, 0.3],
            }}
            transition={{ 
              duration: 4, 
              repeat: Infinity, 
              repeatType: 'reverse' 
            }}
          />
          <motion.div 
            className="absolute inset-0 bg-[radial-gradient(circle_at_70%_50%,rgba(16,185,129,0.15),transparent_50%)]"
            animate={{ 
              opacity: [0.6, 0.3, 0.6],
            }}
            transition={{ 
              duration: 4, 
              repeat: Infinity, 
              repeatType: 'reverse',
              delay: 2
            }}
          />
          
          {/* Glassmorphic card */}
          <motion.div 
            className="relative backdrop-blur-xl bg-gradient-to-br from-card/80 via-card/60 to-card/80 border border-primary/20 rounded-3xl p-8 sm:p-12 shadow-2xl will-change-transform"
            whileHover={{ 
              scale: 1.02,
              boxShadow: '0 25px 50px -12px rgba(107, 70, 193, 0.25)'
            }}
            transition={{ duration: 0.3 }}
          >
            {/* Animated border glow */}
            <motion.div 
              className="absolute inset-0 rounded-3xl bg-gradient-to-br from-purple-500/20 via-transparent to-emerald-500/20"
              animate={{ 
                opacity: [0.3, 0.6, 0.3],
              }}
              transition={{ 
                duration: 3, 
                repeat: Infinity, 
                repeatType: 'reverse' 
              }}
            />
            
            <div className="relative text-center">
              <motion.h3 
                className="text-3xl sm:text-4xl md:text-5xl font-bold mb-6 leading-tight"
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.2, duration: 0.5 }}
              >
                <motion.span
                  className="bg-gradient-to-r from-purple-400 via-purple-600 to-emerald-500 bg-clip-text text-transparent inline-block"
                  animate={{ 
                    backgroundPosition: ['0% 50%', '100% 50%', '0% 50%'],
                  }}
                  transition={{ 
                    duration: 5, 
                    repeat: Infinity,
                    ease: 'linear'
                  }}
                  style={{ 
                    backgroundSize: '200% 200%',
                    filter: 'drop-shadow(0 0 20px rgba(107, 70, 193, 0.3))'
                  }}
                >
                  Let's build something together
                </motion.span>
              </motion.h3>
              
              <motion.p 
                className="text-muted-foreground text-base sm:text-lg mb-8 max-w-2xl mx-auto leading-relaxed"
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.3, duration: 0.5 }}
              >
                I'm always interested in hearing about new projects and opportunities. Let's create something amazing!
              </motion.p>
              
              <motion.div 
                className="flex flex-col sm:flex-row gap-4 justify-center"
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.4, duration: 0.5 }}
              >
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  transition={{ duration: 0.2 }}
                >
                  <Button
                    size="lg"
                    onClick={() => window.location.href = `mailto:${personal.email}`}
                    className="shadow-glow hover:shadow-glow-lg transition-all duration-300 text-base sm:text-lg px-8 py-6 bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-500 hover:to-purple-600 relative overflow-hidden group"
                  >
                    <motion.div
                      className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0"
                      initial={{ x: '-100%' }}
                      whileHover={{ x: '100%' }}
                      transition={{ duration: 0.6 }}
                    />
                    <Mail className="h-5 w-5 mr-2 relative z-10" aria-hidden="true" />
                    <span className="relative z-10">Get in Touch</span>
                  </Button>
                </motion.div>
                
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  transition={{ duration: 0.2 }}
                >
                  <Button
                    size="lg"
                    variant="outline"
                    onClick={() => window.open('/resume.pdf', '_blank', 'noopener,noreferrer')}
                    className="border-2 border-primary/50 hover:border-primary text-base sm:text-lg px-8 py-6 hover:bg-primary/10 backdrop-blur-sm relative overflow-hidden group"
                  >
                    <motion.div
                      className="absolute inset-0 bg-gradient-to-r from-purple-500/0 via-purple-500/10 to-purple-500/0"
                      initial={{ x: '-100%' }}
                      whileHover={{ x: '100%' }}
                      transition={{ duration: 0.6 }}
                    />
                    <Download className="h-5 w-5 mr-2 relative z-10" aria-hidden="true" />
                    <span className="relative z-10">Download Resume</span>
                  </Button>
                </motion.div>
              </motion.div>
            </div>
          </motion.div>
        </motion.div>

        {/* Divider */}
        <div className="border-t border-border mb-8" />

        {/* Footer Content */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          {/* About */}
          <div>
            <h4 className="text-lg font-bold font-mono text-primary mb-4">&lt;RR /&gt;</h4>
            <p className="text-sm text-muted-foreground">
              Full Stack Developer specializing in AI-powered applications and modern web technologies.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-sm font-semibold mb-4 text-foreground">Quick Links</h4>
            <div className="space-y-2 text-sm">
              <motion.button
                onClick={() => document.getElementById('experience')?.scrollIntoView({ behavior: 'smooth' })}
                className="block text-muted-foreground hover:text-primary transition-colors will-change-transform"
                whileHover={{ scale: 1.05, x: 4 }}
                whileTap={{ scale: 0.95 }}
                transition={{ duration: 0.2 }}
              >
                Experience
              </motion.button>
              <motion.button
                onClick={() => document.getElementById('projects')?.scrollIntoView({ behavior: 'smooth' })}
                className="block text-muted-foreground hover:text-primary transition-colors will-change-transform"
                whileHover={{ scale: 1.05, x: 4 }}
                whileTap={{ scale: 0.95 }}
                transition={{ duration: 0.2 }}
              >
                Projects
              </motion.button>
              <motion.button
                onClick={() => document.getElementById('skills')?.scrollIntoView({ behavior: 'smooth' })}
                className="block text-muted-foreground hover:text-primary transition-colors will-change-transform"
                whileHover={{ scale: 1.05, x: 4 }}
                whileTap={{ scale: 0.95 }}
                transition={{ duration: 0.2 }}
              >
                Skills
              </motion.button>
            </div>
          </div>

          {/* Connect */}
          <div>
            <h4 className="text-sm font-semibold mb-4 text-foreground">Connect</h4>
            <div className="flex space-x-4 mb-4" role="list" aria-label="Social media links">
              <motion.a
                href={personal.github}
                target="_blank"
                rel="noopener noreferrer"
                className="text-muted-foreground hover:text-primary transition-colors p-2 hover:bg-primary/10 rounded-lg will-change-transform"
                aria-label="Visit GitHub profile (opens in new tab)"
                role="listitem"
                whileHover={{ scale: 1.1, rotate: 5 }}
                whileTap={{ scale: 0.95 }}
                transition={{ duration: 0.2 }}
              >
                <Github className="h-5 w-5" aria-hidden="true" />
              </motion.a>
              <motion.a
                href={personal.linkedin}
                target="_blank"
                rel="noopener noreferrer"
                className="text-muted-foreground hover:text-primary transition-colors p-2 hover:bg-primary/10 rounded-lg will-change-transform"
                aria-label="Visit LinkedIn profile (opens in new tab)"
                role="listitem"
                whileHover={{ scale: 1.1, rotate: 5 }}
                whileTap={{ scale: 0.95 }}
                transition={{ duration: 0.2 }}
              >
                <Linkedin className="h-5 w-5" aria-hidden="true" />
              </motion.a>
              <motion.a
                href={`mailto:${personal.email}`}
                className="text-muted-foreground hover:text-primary transition-colors p-2 hover:bg-primary/10 rounded-lg will-change-transform"
                aria-label={`Send email to ${personal.email}`}
                role="listitem"
                whileHover={{ scale: 1.1, rotate: 5 }}
                whileTap={{ scale: 0.95 }}
                transition={{ duration: 0.2 }}
              >
                <Mail className="h-5 w-5" aria-hidden="true" />
              </motion.a>
            </div>
            <p className="text-sm text-muted-foreground">
              {personal.email}
            </p>
          </div>
        </div>

        {/* Copyright */}
        <div className="text-center pt-8 border-t border-border">
          <p className="text-sm text-muted-foreground flex items-center justify-center gap-2">
            © {new Date().getFullYear()} {personal.name}. Built with
            <Heart className="h-4 w-4 text-primary fill-primary" aria-hidden="true" />
            using React, TypeScript & FastAPI
          </p>
        </div>
      </div>
    </footer>
  );
};
