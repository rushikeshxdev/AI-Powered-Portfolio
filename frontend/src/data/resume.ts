import type { ResumeData } from '../types';

export const resumeData: ResumeData = {
  "personal": {
    "name": "Rushikesh Randive",
    "email": "rushirandive31@gmail.com",
    "linkedin": "https://www.linkedin.com/in/rushikeshrandive12/",
    "github": "https://github.com/rushikeshxdev",
    "location": "India"
  },
  "education": [
    {
      "institution": "KIT College",
      "qualification": "B.Tech in Computer Science",
      "score": "7.5/10 CGPA",
      "year": "Expected May 2026",
      "relevant_coursework": [
        "Data Structures and Algorithms",
        "Database Management Systems",
        "Machine Learning",
        "Web Development",
        "Software Engineering"
      ]
    },
    {
      "institution": "Netaji Science Jr College Mohol, Solapur",
      "qualification": "HSC",
      "score": "89.67%",
      "year": "2021"
    },
    {
      "institution": "RIKP Mohol, Solapur",
      "qualification": "SSC",
      "score": "88.80%",
      "year": "2019"
    }
  ],
  "experience": [
    {
      "company": "Everything About AI",
      "role": "Full Stack Developer Intern",
      "duration": "Current",
      "location": "Remote",
      "responsibilities": [
        "Developing AI-powered applications using Large Language Models and Generative AI",
        "Building full-stack web applications with React, TypeScript, and FastAPI",
        "Implementing RAG (Retrieval-Augmented Generation) systems for knowledge retrieval",
        "Integrating various AI APIs including Google Gemini and OpenRouter",
        "Designing and deploying production-ready applications with modern DevOps practices"
      ],
      "technologies": [
        "Python",
        "FastAPI",
        "React",
        "TypeScript",
        "Google Gemini API",
        "RAG Systems",
        "Vector Databases"
      ]
    }
  ],
  "skills": {
    "languages": [
      "Python",
      "JavaScript",
      "TypeScript",
      "C++",
      "Java"
    ],
    "frontend": [
      "React.js",
      "Redux",
      "Tailwind CSS",
      "HTML/CSS",
      "Framer Motion"
    ],
    "backend": [
      "Node.js",
      "Express.js",
      "FastAPI",
      "REST APIs"
    ],
    "databases": [
      "PostgreSQL",
      "MongoDB",
      "Prisma ORM",
      "SQLAlchemy"
    ],
    "devops": [
      "Docker",
      "Git",
      "GitHub Actions",
      "CI/CD"
    ],
    "ai_ml": [
      "Google Gemini API",
      "OpenRouter",
      "RAG Systems",
      "Vector Databases",
      "Sentence Transformers"
    ]
  },
  "projects": [
    {
      "name": "HireeFlow.ai",
      "subtitle": "Real-Time Interview Platform with AI Copilot",
      "description": "Engineered a comprehensive technical interview platform combining real-time video conferencing, collaborative code editing, and AI-powered assistance. Built a low-latency video and audio system using WebRTC and simple-peer. Integrated Monaco Editor with Socket.io for simultaneous code editing across 8+ languages. Leveraged Google Gemini 2.0 Flash model for AI Copilot generating context-aware interview questions. Implemented Piston API for secure code compilation.",
      "technologies": [
        "React.js",
        "Node.js",
        "WebRTC",
        "Socket.io",
        "Google Gemini API",
        "Docker",
        "Monaco Editor",
        "Piston API"
      ],
      "github": "https://github.com/rushikeshxdev/HireeFlow.ai",
      "highlights": [
        "Real-Time Communication: Built a low-latency video and audio system using WebRTC and simple-peer",
        "Collaborative Environment: Integrated Monaco Editor with Socket.io for simultaneous code editing across 8+ languages",
        "AI Integration: Leveraged Google Gemini 2.0 Flash model for AI Copilot generating context-aware interview questions",
        "Code Execution: Implemented Piston API for secure code compilation and execution"
      ],
      "skills_demonstrated": [
        "WebRTC",
        "Socket.io",
        "Real-time collaboration",
        "Generative AI",
        "Full-stack development"
      ]
    },
    {
      "name": "DevTranslator",
      "subtitle": "AI-Powered Chrome Extension",
      "description": "Built a zero-latency browser extension that translates informal developer slang (Hinglish) into professional corporate English using Generative AI. Developed using Plasmo framework and Manifest V3. Implemented Server-Sent Events (SSE) to stream translation tokens from Gemini 1.5 Flash API, reducing perceived latency to under 200ms. Utilized Shadow DOM to inject translation UI without conflicting with host site CSS. Designed privacy-first BYOK (Bring Your Own Key) system where API keys are stored locally.",
      "technologies": [
        "TypeScript",
        "React",
        "Chrome Extension API",
        "Google Gemini API",
        "Plasmo Framework",
        "Shadow DOM",
        "Server-Sent Events"
      ],
      "github": "https://github.com/rushikeshxdev/dev-translator",
      "highlights": [
        "Browser Engineering: Developed using Plasmo framework and Manifest V3",
        "Streaming AI Responses: Implemented Server-Sent Events (SSE) to stream translation tokens, reducing perceived latency to under 200ms",
        "Shadow DOM Injection: Utilized Shadow DOM to inject translation UI without conflicting with host site CSS",
        "Privacy-First Architecture: Designed BYOK (Bring Your Own Key) system where API keys are stored locally"
      ],
      "skills_demonstrated": [
        "Browser Extensions",
        "Generative AI",
        "TypeScript",
        "Real-time streaming",
        "Privacy-focused design"
      ]
    },
    {
      "name": "Enterprise Store Rating Platform",
      "subtitle": "RBAC & Security",
      "description": "Developed a production-ready store management system focusing on enterprise-grade security and role management. Architected strict permission system for Admin, Store Owner, and User roles. Implemented JWT authentication with HttpOnly cookies, Bcrypt password hashing (12 salt rounds), and SQL injection protection using Prisma ORM. Achieved high code reliability with 277 passing tests using Jest and Fast-check for property-based testing. Optimized complex SQL queries via Prisma.",
      "technologies": [
        "PostgreSQL",
        "Express.js",
        "React",
        "Prisma ORM",
        "Jest",
        "Fast-check",
        "JWT",
        "Bcrypt"
      ],
      "github": "https://github.com/rushikeshxdev/store-rating-platform",
      "highlights": [
        "Role-Based Access Control (RBAC): Architected strict permission system for Admin, Store Owner, and User roles",
        "Advanced Security: Implemented JWT authentication with HttpOnly cookies, Bcrypt password hashing (12 salt rounds), SQL injection protection",
        "Testing & Quality Assurance: Achieved high code reliability with 277 passing tests using Jest and Fast-check for property-based testing",
        "Performance: Optimized complex SQL queries via Prisma ORM"
      ],
      "skills_demonstrated": [
        "PostgreSQL",
        "Role-Based Access Control (RBAC)",
        "Security",
        "Property-based testing",
        "Enterprise architecture"
      ]
    },
    {
      "name": "FinTrack Pro",
      "subtitle": "Financial Dashboard with MongoDB Optimization",
      "description": "Created a full-stack finance management application designed to handle complex transaction data visualization. Implemented Compound Indexing in MongoDB (sorting by UserID + Date), reducing query execution time by approximately 40%. Integrated Chart.js with Redux Toolkit for real-time interactive financial insights. Centralized application state using Redux. Built robust login system using JWT and secure cookie storage.",
      "technologies": [
        "MongoDB",
        "Express.js",
        "React",
        "Node.js",
        "Redux Toolkit",
        "Chart.js",
        "JWT"
      ],
      "github": "https://github.com/rushikeshxdev/fintrak",
      "highlights": [
        "Database Performance: Implemented Compound Indexing in MongoDB (sorting by UserID + Date), reducing query execution time by ~40%",
        "Data Visualization: Integrated Chart.js with Redux Toolkit for real-time interactive financial insights",
        "State Management: Centralized application state using Redux Toolkit",
        "Secure Authentication: Built robust login system using JWT and secure cookie storage"
      ],
      "skills_demonstrated": [
        "MongoDB",
        "Database Optimization",
        "Redux",
        "Data visualization",
        "Performance tuning"
      ]
    },
    {
      "name": "Gmail to Google Sheets Automation",
      "subtitle": "Automated Workflow Integration",
      "description": "Designed and deployed a Python automation bot to streamline data entry workflows by syncing email data to spreadsheets. Implemented secure authentication using OAuth 2.0 via Google Cloud Console. Engineered state-persistence mechanism using atomic file operations (JSON) to track processed email IDs and prevent duplicates. Utilized BeautifulSoup to parse complex HTML email bodies. Achieved 100% success rate in processing 300+ emails during stress testing.",
      "technologies": [
        "Python",
        "Google Gmail API",
        "Google Sheets API",
        "OAuth 2.0",
        "BeautifulSoup",
        "JSON"
      ],
      "github": "https://github.com/rushikeshxdev/gmail-to-sheets-automation",
      "highlights": [
        "OAuth 2.0 Security: Implemented secure authentication using Google Cloud Console",
        "Duplicate Prevention: Engineered state-persistence mechanism using atomic file operations (JSON) to track processed email IDs",
        "Data Parsing: Utilized BeautifulSoup to parse complex HTML email bodies",
        "Reliability: Achieved 100% success rate in processing 300+ emails during stress testing"
      ],
      "skills_demonstrated": [
        "Python",
        "Workflow Automation",
        "API Integration",
        "OAuth 2.0",
        "Data parsing"
      ]
    },
    {
      "name": "InternVerse - Smart Internship Portal",
      "subtitle": "MERN Stack Internship Management System",
      "description": "Full-stack role-based web application that streamlines the entire internship lifecycle from application to certificate generation. Features separate portals for Interns and Admins with complete CRUD operations, automated workflows, and real-time status tracking.",
      "technologies": [
        "React.js",
        "Node.js",
        "Express.js",
        "MongoDB",
        "JWT",
        "Tailwind CSS"
      ],
      "github": "https://github.com/rushikeshxdev/InternVerse",
      "highlights": [
        "Role-Based Access Control (RBAC) with separate portals for Interns and Admins",
        "RESTful API Design with clean, scalable architecture",
        "Automated email notifications and certificate generation",
        "Real-time application status tracking (Pending, Approved, Rejected)"
      ],
      "skills_demonstrated": [
        "MERN Stack",
        "RBAC",
        "RESTful APIs",
        "Workflow Automation",
        "JWT Authentication"
      ]
    },
    {
      "name": "Airbnb Sales Analysis",
      "subtitle": "Power BI Data Analytics Dashboard",
      "description": "Comprehensive Power BI project analyzing Airbnb sales data to provide insights into sales performance, trends, and key metrics. Built with interactive visualizations and data modeling for business intelligence.",
      "technologies": [
        "Power BI",
        "Data Analysis",
        "CSV Processing",
        "DAX"
      ],
      "github": "https://github.com/rushikeshxdev/Airbnb-Sales-Analysis",
      "highlights": [
        "Interactive Power BI dashboard with real-time insights",
        "Data modeling and transformation using Power Query",
        "Sales performance metrics and trend analysis",
        "Version-controlled using Power BI Project format (.pbip)"
      ],
      "skills_demonstrated": [
        "Power BI",
        "Data Analysis",
        "Business Intelligence",
        "Data Visualization"
      ]
    },
    {
      "name": "Sales Voice AI Sentiment Analysis",
      "subtitle": "Real-time Sentiment Analysis System",
      "description": "Real-time sentiment analysis system for sales voice AI agents that analyzes customer interactions, providing actionable insights to improve sales performance. Features live dashboard with WebSocket communication and sub-2 second response times.",
      "technologies": [
        "Python",
        "Flask",
        "React",
        "Socket.IO",
        "NLTK",
        "TextBlob",
        "Recharts"
      ],
      "github": "https://github.com/rushikeshxdev/sales-voice-ai-sentiment",
      "highlights": [
        "Real-time sentiment scoring with emotion detection (9 emotional states)",
        "Live dashboard with WebSocket-based updates (< 100ms latency)",
        "Buying signal detection and objection recognition",
        "Performance: < 2 seconds analysis time, 85%+ accuracy"
      ],
      "skills_demonstrated": [
        "Python",
        "Flask",
        "Real-time Systems",
        "NLP",
        "Sentiment Analysis",
        "WebSocket"
      ]
    }
  ],
  "certifications": [
    {
      "name": "Complete DevOps Cohort 3.0",
      "issuer": "100xDevs",
      "issued": "Dec 2025",
      "skills": [
        "DevOps",
        "Docker",
        "Kubernetes",
        "CI/CD",
        "AWS"
      ]
    },
    {
      "name": "Saviynt Identity Security for AI Age",
      "issuer": "Saviynt",
      "issued": "Jan 2026",
      "description": "Completed an 8-CPE-hour certification focusing on Identity Security for the AI Age. Training covered essential strategies for identity and access management (IAM) and AI security.",
      "skills": [
        "IAM",
        "Identity Security",
        "AI Security",
        "Access Management"
      ]
    }
  ]
};
