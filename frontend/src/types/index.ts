// Message types
export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  isStreaming?: boolean;
}

// Chat state types
export interface ChatState {
  sessionId: string;
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  addMessage: (message: Message) => void;
  updateMessage: (id: string, content: string) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearMessages: () => void;
  initializeSession: () => void;
}

// Theme state types
export interface ThemeState {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
}

// Resume data types
export interface PersonalInfo {
  name: string;
  email: string;
  linkedin: string;
  github: string;
  location: string;
}

export interface EducationEntry {
  institution: string;
  qualification: string;
  score: string;
  year: string;
  relevant_coursework?: string[];
}

export interface Experience {
  company: string;
  role: string;
  duration: string;
  location: string;
  responsibilities: string[];
  technologies: string[];
}

export interface Skills {
  languages: string[];
  frontend: string[];
  backend: string[];
  databases: string[];
  devops: string[];
  ai_ml: string[];
}

export interface Project {
  name: string;
  subtitle?: string;
  description: string;
  technologies: string[];
  github?: string;
  demo?: string;
  imageUrl?: string;
  highlights: string[];
  skills_demonstrated: string[];
}

export interface Certification {
  name: string;
  issuer: string;
  issued: string;
  description?: string;
  skills: string[];
}

export interface ResumeData {
  personal: PersonalInfo;
  education: EducationEntry[];
  experience: Experience[];
  skills: Skills;
  projects: Project[];
  certifications: Certification[];
}

// Component props types
export interface ProjectCardProps {
  project: Project;
  index: number;
}

export interface MessageBubbleProps {
  message: Message;
}

export interface SuggestedQuestionProps {
  question: string;
  onClick: (question: string) => void;
}

// API types
export interface ChatRequest {
  question: string;
  session_id: string;
}

export interface ChatHistoryResponse {
  session_id: string;
  messages: Message[];
}

export interface HealthResponse {
  status: string;
  timestamp: string;
  services: {
    database: boolean;
    vector_store: boolean;
  };
}
