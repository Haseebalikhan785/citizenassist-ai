import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck, ExternalLink, Heart } from 'lucide-react';
import { useTranslation } from '../i18n';

export const Footer: React.FC = () => {
  const { t } = useTranslation();

  return (
    <footer className="bg-slate-950 text-slate-400 border-t border-slate-800 text-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Col 1: Identity & Problem Statement */}
          <div className="md:col-span-2">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-6 h-6 rounded-lg bg-blue-600 flex items-center justify-center font-bold text-white text-xs">
                CA
              </div>
              <span className="text-sm font-bold text-white tracking-tight">
                CitizenAssist AI
              </span>
            </div>
            <p className="text-slate-400 text-xs leading-relaxed max-w-md">
              Intelligent Public Service Navigator. Built for GRAVITON 2026 (CGC University, Mohali), Problem Statement #11: Multilingual assistant for public service discovery, eligibility reasoning, document preparation, and official link verification.
            </p>
            <div className="mt-4 p-3 bg-slate-900 border border-slate-800 rounded-xl flex items-start gap-2.5">
              <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <p className="text-[11px] text-slate-300 leading-snug">
                <strong className="text-white">Strict Disclaimer:</strong> {t('footer.disclaimer')}
              </p>
            </div>
          </div>

          {/* Col 2: Navigation */}
          <div>
            <h4 className="text-xs font-semibold text-white uppercase tracking-wider mb-3">
              Explore
            </h4>
            <ul className="space-y-2">
              <li>
                <Link to="/schemes" className="hover:text-white transition">
                  {t('nav.schemes')}
                </Link>
              </li>
              <li>
                <Link to="/assistant" className="hover:text-white transition">
                  {t('nav.assistant')}
                </Link>
              </li>
              <li>
                <Link to="/eligibility" className="hover:text-white transition">
                  {t('nav.eligibility')}
                </Link>
              </li>
              <li>
                <Link to="/compare" className="hover:text-white transition">
                  {t('nav.compare')}
                </Link>
              </li>
              <li>
                <Link to="/about" className="hover:text-white transition">
                  {t('nav.about')}
                </Link>
              </li>
            </ul>
          </div>

          {/* Col 3: Official Portals */}
          <div>
            <h4 className="text-xs font-semibold text-white uppercase tracking-wider mb-3">
              Official Portals
            </h4>
            <ul className="space-y-2">
              <li>
                <a
                  href="https://www.myscheme.gov.in"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-white transition flex items-center gap-1"
                >
                  myScheme.gov.in <ExternalLink className="w-3 h-3 text-slate-500" />
                </a>
              </li>
              <li>
                <a
                  href="https://scholarships.gov.in"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-white transition flex items-center gap-1"
                >
                  National Scholarship Portal <ExternalLink className="w-3 h-3 text-slate-500" />
                </a>
              </li>
              <li>
                <a
                  href="https://india.gov.in"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-white transition flex items-center gap-1"
                >
                  National Portal of India <ExternalLink className="w-3 h-3 text-slate-500" />
                </a>
              </li>
              <li>
                <a
                  href="https://punjab.gov.in"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-white transition flex items-center gap-1"
                >
                  Government of Punjab Portal <ExternalLink className="w-3 h-3 text-slate-500" />
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="pt-6 border-t border-slate-900 flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px] text-slate-500">
          <p>© 2026 CitizenAssist AI • Independent Hackathon Project for GRAVITON 2026</p>
          <div className="flex items-center gap-4">
            <Link to="/about" className="hover:text-slate-400">
              Architecture & Problem Statement #11
            </Link>
            <span>•</span>
            <span className="flex items-center gap-1">
              Crafted with <Heart className="w-3 h-3 text-red-500" /> for Indian Citizens
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
};
