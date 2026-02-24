import React from 'react';
import { motion } from 'framer-motion';
import type { Variants } from 'framer-motion';
import { ArrowLeft, Sparkles, TrendingUp, Zap, Code2, Brain, Rocket, Users, Target, Mail, Github, Linkedin } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { resumeData } from '../data/resume';
import { Button } from '../components/ui/Button';
import { useReducedMotion } from '../hooks/useReducedMotion';

export const Introduction: React.FC = () => {
  const navigate = useNavigate();
  const prefersReducedMotion = useReducedMotion();

  const containerVariants: Variants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2
      }
    }
  };

  const itemVariants: Variants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.5 }
    }
  };

  const stats = [
    { label: '8+ Production Apps', icon: Rocket },
    { label: 'Real-Time Systems', icon: Zap },
    { label: '1000+ Active Users', icon: Users },
    { label: '<200ms Latency', icon: TrendingUp }
  ];

  const skills = [
    {
      title: 'AI & Automation',
      description: 'RAG, Gemini, OpenRouter, Vector DBs',
      icon: Brain
    },
    {
      title: 'Performance Engineering',
      description: 'WebRTC, Socket.io, real-time systems',
      icon: Zap
    },
    {
      title: 'System Architecture',
      description: 'Docker, PostgreSQL, MongoDB, microservices',
      icon: Code2
    },
    {
      title: 'Production Mindset',
      description: 'JWT, RBAC, security best practices',
      icon: Target
    },
    {
      title: 'Fast Learner',
      description: '100xDevs graduate, Saviynt certified',
      icon: TrendingUp
    },
    {
      title: 'Team Player',
      description: 'Git workflows, documentation, collaboration',
      icon: Users
    },
    {
      title: 'Problem Solver',
      description: 'Full-stack development, complex challenges',
      icon: Sparkles
    },
    {
      title: 'Full Stack Versatility',
      description: 'React, TypeScript, Node.js, FastAPI, Python',
      icon: Rocket
    }
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Header with back button */}
      <header className="sticky top-0 z-50 bg-background/80 backdrop-blur-md border-b border-border">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <Button
            variant="ghost"
            onClick={() => navigate('/')}
            className="flex items-center gap-2"
            aria-label="Back to home"
          >
            <ArrowLeft className="h-5 w-5" aria-hidden="true" />
            Back to Home
          </Button>
        </div>
      </header>

      {/* Main content */}
      <main className="py-12 sm:py-16 md:py-20">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-5xl">
          <motion.div
            initial="hidden"
            animate="visible"
            variants={prefersReducedMotion ? undefined : containerVariants}
            className="space-y-16 sm:space-y-20"
          >
            {/* Hero Section */}
            <motion.section variants={prefersReducedMotion ? undefined : itemVariants} className="text-center space-y-6">
              <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold bg-gradient-to-r from-primary via-purple-500 to-pink-500 bg-clip-text text-transparent">
                Hi, I'm Rushikesh Randive
              </h1>
              <p className="text-xl sm:text-2xl text-muted-foreground font-medium">
                Building AI-Powered Full Stack Applications
              </p>
              <p className="text-base sm:text-lg text-muted-foreground max-w-3xl mx-auto leading-relaxed">
                I specialize in crafting production-ready applications that blend cutting-edge AI/ML technologies with robust full-stack engineering. 
                From real-time collaboration systems to RAG-powered intelligent platforms, I turn complex technical challenges into elegant, scalable solutions.
              </p>
            </motion.section>

            {/* Availability Badge */}
            <motion.section variants={prefersReducedMotion ? undefined : itemVariants} className="flex justify-center">
              <div className="glassmorphism px-6 py-4 rounded-2xl border-2 border-primary/30 inline-block">
                <div className="flex items-center gap-3">
                  <span className="relative flex h-3 w-3">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
                  </span>
                  <div className="text-left">
                    <p className="font-bold text-foreground">Available for Opportunities</p>
                    <p className="text-sm text-muted-foreground">Remote • Internship • Full-Time Ready</p>
                  </div>
                </div>
              </div>
            </motion.section>

            {/* My Journey Section */}
            <motion.section variants={prefersReducedMotion ? undefined : itemVariants} className="space-y-6">
              <h2 className="text-3xl sm:text-4xl font-bold text-center">From Curiosity to Production</h2>
              <div className="glassmorphism p-6 sm:p-8 rounded-2xl space-y-4 text-muted-foreground leading-relaxed">
                <p>
                  My journey into software engineering started with curiosity and evolved into a passion for building systems that matter. 
                  Currently working as a <span className="text-primary font-semibold">Full Stack Developer Intern at Everything About AI</span>, 
                  I'm developing AI-powered applications using Large Language Models, implementing RAG systems, and integrating cutting-edge APIs like Google Gemini and OpenRouter.
                </p>
                <p>
                  I've shipped <span className="text-primary font-semibold">8+ production applications</span> that serve over 1000 active users, including 
                  <span className="text-primary font-semibold"> HireeFlow.ai</span> (a real-time interview platform with WebRTC and AI copilot), 
                  <span className="text-primary font-semibold"> DevTranslator</span> (a Chrome extension with sub-200ms latency using streaming AI), 
                  and enterprise-grade systems with RBAC and advanced security.
                </p>
                <p>
                  I'm in my <span className="text-primary font-semibold">final year at KIT College</span> pursuing B.Tech in Computer Science (7.5 CGPA, graduating May 2026). 
                  I've completed the <span className="text-primary font-semibold">100xDevs DevOps Cohort 3.0</span> and earned the 
                  <span className="text-primary font-semibold"> Saviynt Identity Security for AI Age</span> certification, constantly expanding my expertise in modern development practices.
                </p>
              </div>
            </motion.section>

            {/* Stats Grid */}
            <motion.section variants={prefersReducedMotion ? undefined : itemVariants}>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6">
                {stats.map((stat, index) => {
                  const Icon = stat.icon;
                  return (
                    <div
                      key={index}
                      className="glassmorphism p-6 rounded-2xl text-center space-y-3 hover:border-primary/50 transition-all duration-300"
                    >
                      <Icon className="h-8 w-8 text-primary mx-auto" aria-hidden="true" />
                      <p className="font-bold text-foreground text-sm sm:text-base">{stat.label}</p>
                    </div>
                  );
                })}
              </div>
            </motion.section>

            {/* What I Bring Section */}
            <motion.section variants={prefersReducedMotion ? undefined : itemVariants} className="space-y-8">
              <h2 className="text-3xl sm:text-4xl font-bold text-center">More Than Just Code</h2>
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
                {skills.map((skill, index) => {
                  const Icon = skill.icon;
                  return (
                    <div
                      key={index}
                      className="glassmorphism p-6 rounded-2xl space-y-3 hover:border-primary/50 hover:shadow-glow transition-all duration-300"
                    >
                      <Icon className="h-6 w-6 text-primary" aria-hidden="true" />
                      <h3 className="font-bold text-foreground text-lg">{skill.title}</h3>
                      <p className="text-sm text-muted-foreground">{skill.description}</p>
                    </div>
                  );
                })}
              </div>
            </motion.section>

            {/* Open to Opportunities Section */}
            <motion.section variants={prefersReducedMotion ? undefined : itemVariants} className="space-y-6">
              <h2 className="text-3xl sm:text-4xl font-bold text-center">Let's Build Something Great Together</h2>
              <div className="glassmorphism p-6 sm:p-8 rounded-2xl space-y-6">
                <p className="text-center text-lg text-muted-foreground">
                  <span className="text-primary font-semibold">Full Stack Engineer</span> • 
                  <span className="text-primary font-semibold"> AI/ML Engineer</span> • 
                  <span className="text-primary font-semibold"> Backend Engineer</span>
                </p>
                <ul className="space-y-3 max-w-2xl mx-auto">
                  <li className="flex items-start gap-3 text-muted-foreground">
                    <span className="text-primary font-bold mt-1" aria-hidden="true">✓</span>
                    <span>Remote-first or open to relocation in India</span>
                  </li>
                  <li className="flex items-start gap-3 text-muted-foreground">
                    <span className="text-primary font-bold mt-1" aria-hidden="true">✓</span>
                    <span>Available to start immediately</span>
                  </li>
                  <li className="flex items-start gap-3 text-muted-foreground">
                    <span className="text-primary font-bold mt-1" aria-hidden="true">✓</span>
                    <span>Graduating May 2026 (Final Year BTech)</span>
                  </li>
                </ul>
                <div className="flex justify-center pt-4">
                  <Button
                    onClick={() => window.open(`https://www.linkedin.com/in/rushikeshrandive12/messaging/`, '_blank')}
                    className="px-8 py-6 text-lg font-semibold bg-gradient-to-r from-primary to-purple-600 hover:from-primary/90 hover:to-purple-600/90"
                    aria-label="Send email to Rushikesh Randive"
                  >
                    Let's Talk →
                  </Button>
                </div>
              </div>
            </motion.section>

            {/* Connect Section */}
            <motion.section variants={prefersReducedMotion ? undefined : itemVariants} className="space-y-6">
              <div className="text-center space-y-4">
                <h2 className="text-3xl sm:text-4xl font-bold">Let's build something together</h2>
                <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                  Always interested in collaborations, interesting problems, and conversations about code, design, and everything in between.
                </p>
                <Button
                  variant="outline"
                  onClick={() => window.open(`https://www.linkedin.com/in/rushikeshrandive12/messaging/`, '_blank')}
                  className="mt-4 px-6 py-6 text-base font-semibold border-2 border-primary/50 hover:bg-primary/10"
                  aria-label="Send a signal via email"
                >
                  send a signal →
                </Button>
              </div>
            </motion.section>

            {/* Find Me Elsewhere */}
            <motion.section variants={prefersReducedMotion ? undefined : itemVariants} className="space-y-6">
              <h3 className="text-2xl font-bold text-center">Find Me Elsewhere</h3>
              <div className="flex justify-center gap-6">
                <a
                  href={resumeData.personal.github}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="social-icon glassmorphism p-4 rounded-xl"
                  aria-label="Visit GitHub profile"
                >
                  <Github className="h-6 w-6" aria-hidden="true" />
                </a>
                <a
                  href={resumeData.personal.linkedin}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="social-icon glassmorphism p-4 rounded-xl"
                  aria-label="Visit LinkedIn profile"
                >
                  <Linkedin className="h-6 w-6" aria-hidden="true" />
                </a>
                <a
                  href={`mailto:${resumeData.personal.email}`}
                  className="social-icon glassmorphism p-4 rounded-xl"
                  aria-label="Send email"
                >
                  <Mail className="h-6 w-6" aria-hidden="true" />
                </a>
              </div>
            </motion.section>

            {/* Footer */}
            <motion.footer variants={prefersReducedMotion ? undefined : itemVariants} className="text-center space-y-2 pt-8 border-t border-border">
              <p className="text-muted-foreground">Forged with ❤️ & code</p>
              <p className="text-sm text-muted-foreground">© 2026 Rushikesh Randive — All rights reserved</p>
            </motion.footer>
          </motion.div>
        </div>
      </main>
    </div>
  );
};
