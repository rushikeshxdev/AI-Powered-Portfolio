import { useEffect, lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useThemeStore } from './stores/themeStore';
import { ErrorBoundary } from './components/ErrorBoundary';
import { Header } from './components/Header';
import { Hero } from './components/Hero';
import { Footer } from './components/Footer';
import { FloatingChatbot } from './components/FloatingChatbot';
import { ScrollProgress } from './components/ScrollProgress';
import { Skeleton } from './components/ui/Skeleton';
import { Introduction } from './pages/Introduction';

// Lazy load heavy components for better performance
const About = lazy(() => import('./components/About').then(module => ({ default: module.About })));
const Projects = lazy(() => import('./components/Projects').then(module => ({ default: module.Projects })));
const Skills = lazy(() => import('./components/Skills').then(module => ({ default: module.Skills })));
const Certifications = lazy(() => import('./components/Certifications').then(module => ({ default: module.Certifications })));
const Education = lazy(() => import('./components/Education').then(module => ({ default: module.Education })));

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      refetchOnWindowFocus: false,
    },
  },
});

function HomePage() {
  return (
    <>
      <ScrollProgress />
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-primary focus:text-primary-foreground focus:rounded-md focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
      >
        Skip to main content
      </a>
      <Header />
      <main id="main-content">
        <Hero />
        <Suspense fallback={
          <section className="py-16 px-4 sm:px-6 lg:px-8">
            <div className="max-w-6xl mx-auto space-y-4">
              <Skeleton className="h-8 w-48 mx-auto" />
              <Skeleton className="h-24 w-full" />
            </div>
          </section>
        }>
          <About />
        </Suspense>
        <Suspense fallback={
          <section className="py-16 px-4 sm:px-6 lg:px-8 bg-muted/30">
            <div className="max-w-6xl mx-auto">
              <Skeleton className="h-8 w-48 mx-auto mb-8" />
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Skeleton className="h-64 w-full" />
                <Skeleton className="h-64 w-full" />
                <Skeleton className="h-64 w-full" />
                <Skeleton className="h-64 w-full" />
              </div>
            </div>
          </section>
        }>
          <Projects />
        </Suspense>
        <Suspense fallback={
          <section className="py-16 px-4 sm:px-6 lg:px-8">
            <div className="max-w-6xl mx-auto space-y-4">
              <Skeleton className="h-8 w-48 mx-auto mb-8" />
              <Skeleton className="h-32 w-full" />
            </div>
          </section>
        }>
          <Skills />
        </Suspense>
        <Suspense fallback={
          <section className="py-16 px-4 sm:px-6 lg:px-8 bg-muted/30">
            <div className="max-w-6xl mx-auto">
              <Skeleton className="h-8 w-48 mx-auto mb-8" />
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Skeleton className="h-64 w-full" />
                <Skeleton className="h-64 w-full" />
              </div>
            </div>
          </section>
        }>
          <Certifications />
        </Suspense>
        <Suspense fallback={
          <section className="py-16 px-4 sm:px-6 lg:px-8">
            <div className="max-w-6xl mx-auto">
              <Skeleton className="h-8 w-48 mx-auto mb-8" />
              <Skeleton className="h-64 w-full" />
            </div>
          </section>
        }>
          <Education />
        </Suspense>
      </main>
      <Footer />
      <FloatingChatbot />
    </>
  );
}

function App() {
  const { theme } = useThemeStore();

  useEffect(() => {
    // Apply theme on mount
    document.documentElement.classList.remove('light', 'dark');
    document.documentElement.classList.add(theme);
  }, [theme]);

  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <div className="min-h-screen bg-background text-foreground">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/introduction" element={<Introduction />} />
            </Routes>
          </div>
        </BrowserRouter>
      </QueryClientProvider>
    </ErrorBoundary>
  );
}

export default App;
