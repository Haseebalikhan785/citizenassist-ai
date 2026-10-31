import React, { createContext, useContext, useEffect, useState } from 'react';
import en from './en.json';
import hi from './hi.json';
import pa from './pa.json';

export type Language = 'en' | 'hi' | 'pa';

const translations: Record<Language, any> = {
  en,
  hi,
  pa,
};

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: (path: string, params?: Record<string, any>) => string;
}

const LanguageContext = createContext<LanguageContextType>({
  language: 'en',
  setLanguage: () => {},
  t: (path: string) => path,
});

export const LanguageProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [language, setLanguageState] = useState<Language>(() => {
    const saved = localStorage.getItem('citizenassist_lang') as Language;
    return saved === 'hi' || saved === 'pa' ? saved : 'en';
  });

  const setLanguage = (lang: Language) => {
    setLanguageState(lang);
    localStorage.setItem('citizenassist_lang', lang);
  };

  const t = (path: string, params?: Record<string, any>): string => {
    const keys = path.split('.');
    let val: any = translations[language];

    for (const key of keys) {
      if (val && typeof val === 'object' && key in val) {
        val = val[key];
      } else {
        // Fallback to English
        let fallbackVal: any = translations.en;
        for (const fbKey of keys) {
          if (fallbackVal && typeof fallbackVal === 'object' && fbKey in fallbackVal) {
            fallbackVal = fallbackVal[fbKey];
          } else {
            fallbackVal = path;
            break;
          }
        }
        val = fallbackVal;
        break;
      }
    }

    if (typeof val === 'string' && params) {
      Object.entries(params).forEach(([k, v]) => {
        val = val.replace(new RegExp(`{{${k}}}`, 'g'), String(v));
      });
    }

    return typeof val === 'string' ? val : path;
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useTranslation = () => useContext(LanguageContext);
