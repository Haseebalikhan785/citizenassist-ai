import React from 'react';
import { Shield, Sparkles, Database, FileText, Globe, CheckCircle2, Lock } from 'lucide-react';
import { useTranslation } from '../i18n';

export const About: React.FC = () => {
  const { t } = useTranslation();

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-10">
      {/* Title */}
      <div className="text-center max-w-3xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-50 border border-blue-200 text-blue-700 text-xs font-semibold mb-4">
          <Sparkles className="w-4 h-4 text-blue-600" />
          <span>GRAVITON 2026 • Problem Statement #11</span>
        </div>

        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
          CitizenAssist AI: Intelligent Public Service Navigator
        </h1>
        <p className="text-sm sm:text-base text-slate-600 mt-3 leading-relaxed">
          A multilingual, grounded AI platform helping Indian citizens discover welfare schemes, understand statutory eligibility, prepare document checklists, and navigate official government portals.
        </p>
      </div>

      {/* Mandatory Disclaimer Box */}
      <div className="p-6 bg-slate-900 text-white rounded-3xl shadow-sm border border-slate-800">
        <div className="flex items-start gap-3">
          <Shield className="w-6 h-6 text-emerald-400 shrink-0 mt-1" />
          <div className="space-y-2 text-xs sm:text-sm text-slate-300">
            <h3 className="font-bold text-white text-base">Important Government Data & Affiliation Disclaimer</h3>
            <p>
              CitizenAssist AI is an <strong>independent student hackathon innovation project</strong> built for GRAVITON 2026 at CGC University, Mohali.
            </p>
            <p>
              <strong>Not affiliated with or endorsed by the Government of India or any state government.</strong> We do not use the Government of India emblem, Ashoka symbol, or official seals. Citizens must always verify statutory rules and submit applications exclusively on authentic government portals (<code className="text-blue-300">.gov.in</code> / <code className="text-blue-300">.nic.in</code>).
            </p>
          </div>
        </div>
      </div>

      {/* Required AI Techniques */}
      <section className="space-y-4">
        <h2 className="text-xl font-bold text-slate-900">Required AI Techniques Implemented</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-6 bg-white rounded-3xl border border-slate-200 shadow-sm">
            <div className="w-10 h-10 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center mb-3">
              <Database className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-slate-900">1. Hybrid RAG Pipeline</h3>
            <p className="text-xs text-slate-600 mt-2 leading-relaxed">
              Combines SQLite FTS5 BM25 keyword retrieval (works 100% offline with zero API keys) and dense multilingual vector embeddings with cosine similarity. Chunks preserve section metadata and official URLs.
            </p>
          </div>

          <div className="p-6 bg-white rounded-3xl border border-slate-200 shadow-sm">
            <div className="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center mb-3">
              <Globe className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-slate-900">2. Multilingual NLP</h3>
            <p className="text-xs text-slate-600 mt-2 leading-relaxed">
              Seamlessly handles English, Hindi (हिंदी), and Punjabi (ਪੰਜਾਬੀ). Allows mixed-language citizen inputs, detects profile nuances, and maintains scheme titles in authentic vernacular format with translations.
            </p>
          </div>

          <div className="p-6 bg-white rounded-3xl border border-slate-200 shadow-sm">
            <div className="w-10 h-10 rounded-xl bg-purple-100 text-purple-700 flex items-center justify-center mb-3">
              <FileText className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-slate-900">3. Information Extraction</h3>
            <p className="text-xs text-slate-600 mt-2 leading-relaxed">
              Automated supervised pipeline extracts structured criteria, benefit caps, and document lists from official government circular PDFs (PyMuPDF) and SSRF-safe public URLs into audited draft schemes.
            </p>
          </div>
        </div>
      </section>

      {/* Scope Rule: Four Core Capabilities */}
      <section className="space-y-4">
        <h2 className="text-xl font-bold text-slate-900">The 4 Core Capabilities</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs sm:text-sm">
          <div className="p-4 bg-white rounded-2xl border border-slate-200 shadow-sm flex items-start gap-3">
            <CheckCircle2 className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
            <div>
              <strong className="text-slate-900 block font-bold">1. Locate Relevant Public Services:</strong>
              <span className="text-slate-600">Multi-facet directory of 10 welfare schemes and 4 statutory citizen services across central and state jurisdictions.</span>
            </div>
          </div>

          <div className="p-4 bg-white rounded-2xl border border-slate-200 shadow-sm flex items-start gap-3">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
            <div>
              <strong className="text-slate-900 block font-bold">2. Understand Eligibility Criteria:</strong>
              <span className="text-slate-600">Deterministic rule engine explains rule-by-rule conditions with exact quotations from government documentation.</span>
            </div>
          </div>

          <div className="p-4 bg-white rounded-2xl border border-slate-200 shadow-sm flex items-start gap-3">
            <CheckCircle2 className="w-5 h-5 text-indigo-600 shrink-0 mt-0.5" />
            <div>
              <strong className="text-slate-900 block font-bold">3. Prepare Document Checklists:</strong>
              <span className="text-slate-600">Personalized checklists link directly to citizen services explaining where and how to obtain required documents.</span>
            </div>
          </div>

          <div className="p-4 bg-white rounded-2xl border border-slate-200 shadow-sm flex items-start gap-3">
            <CheckCircle2 className="w-5 h-5 text-purple-600 shrink-0 mt-0.5" />
            <div>
              <strong className="text-slate-900 block font-bold">4. Find Official Application Links:</strong>
              <span className="text-slate-600">Every application portal link is strictly verified and monitored for responsiveness to prevent phishing risks.</span>
            </div>
          </div>
        </div>
      </section>

      {/* Sustainable Development Goals (SDG) Alignment */}
      <section className="bg-slate-100 p-6 rounded-3xl border border-slate-200 space-y-3">
        <h3 className="text-sm font-bold text-slate-900">Sustainable Development Goals (SDG) Alignment (Team Suggestion)</h3>
        <ul className="text-xs text-slate-700 space-y-2">
          <li>• <strong>SDG 1 (No Poverty):</strong> Ensuring social protection benefits reach marginalized citizens, farmers, and students without middleman leakage.</li>
          <li>• <strong>SDG 10 (Reduced Inequalities):</strong> Breaking bureaucratic and linguistic barriers for non-English speakers through Hindi and Punjabi access.</li>
          <li>• <strong>SDG 16 (Peace, Justice and Strong Institutions):</strong> Promoting transparent public access to statutory rules, eligibility criteria, and government portals.</li>
        </ul>
      </section>
    </div>
  );
};
