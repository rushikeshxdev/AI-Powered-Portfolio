import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.tsx';

// Initialize theme before rendering
const savedTheme = localStorage.getItem('theme-storage');
if (savedTheme) {
  try {
    const { state } = JSON.parse(savedTheme);
    if (state?.theme) {
      document.documentElement.classList.add(state.theme);
    }
  } catch (e) {
    // If parsing fails, default to dark
    document.documentElement.classList.add('dark');
  }
} else {
  // Default to dark theme
  document.documentElement.classList.add('dark');
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>
);
