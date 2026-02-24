import React, { useState } from 'react';
import { Palette } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from './ui/Button';

type ColorTheme = 'green' | 'blue' | 'purple' | 'orange';

const themes: Record<ColorTheme, { name: string; primary: string; gradient1: string; gradient2: string; gradient3: string }> = {
  green: {
    name: 'Terminal Green',
    primary: '142 76% 36%',
    gradient1: '142 76% 36%',
    gradient2: '158 64% 52%',
    gradient3: '173 80% 40%',
  },
  blue: {
    name: 'Ocean Blue',
    primary: '217 91% 60%',
    gradient1: '217 91% 60%',
    gradient2: '199 89% 48%',
    gradient3: '187 85% 53%',
  },
  purple: {
    name: 'Royal Purple',
    primary: '271 81% 56%',
    gradient1: '271 81% 56%',
    gradient2: '286 73% 44%',
    gradient3: '250 95% 63%',
  },
  orange: {
    name: 'Sunset Orange',
    primary: '25 95% 53%',
    gradient1: '25 95% 53%',
    gradient2: '16 90% 58%',
    gradient3: '38 92% 50%',
  },
};

export const ThemeSwitcher: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [currentTheme, setCurrentTheme] = useState<ColorTheme>('green');

  const applyTheme = (theme: ColorTheme) => {
    const root = document.documentElement;
    const themeColors = themes[theme];
    
    root.style.setProperty('--primary', themeColors.primary);
    root.style.setProperty('--ring', themeColors.primary);
    root.style.setProperty('--gradient-1', themeColors.gradient1);
    root.style.setProperty('--gradient-2', themeColors.gradient2);
    root.style.setProperty('--gradient-3', themeColors.gradient3);
    
    setCurrentTheme(theme);
    setIsOpen(false);
  };

  return (
    <div className="relative">
      <Button
        variant="ghost"
        size="sm"
        onClick={() => setIsOpen(!isOpen)}
        className="relative"
        aria-label="Change color theme"
        aria-expanded={isOpen}
      >
        <Palette className="h-5 w-5" aria-hidden="true" />
      </Button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.95 }}
            transition={{ duration: 0.15 }}
            className="absolute right-0 mt-2 w-48 glassmorphism rounded-lg shadow-xl border border-border overflow-hidden z-50"
          >
            <div className="p-2">
              <p className="text-xs font-semibold text-muted-foreground px-2 py-1 mb-1">
                Color Theme
              </p>
              {(Object.keys(themes) as ColorTheme[]).map((theme) => (
                <button
                  key={theme}
                  onClick={() => applyTheme(theme)}
                  className={`w-full text-left px-3 py-2 rounded-md text-sm transition-colors flex items-center justify-between ${
                    currentTheme === theme
                      ? 'bg-primary text-primary-foreground'
                      : 'hover:bg-secondary'
                  }`}
                  aria-label={`Switch to ${themes[theme].name} theme`}
                >
                  <span>{themes[theme].name}</span>
                  <div
                    className="h-4 w-4 rounded-full border-2 border-background"
                    style={{ backgroundColor: `hsl(${themes[theme].primary})` }}
                    aria-hidden="true"
                  />
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
