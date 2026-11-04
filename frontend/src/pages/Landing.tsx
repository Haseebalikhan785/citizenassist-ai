import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import {
  GraduationCap,
  Tractor,
  HeartPulse,
  Briefcase,
  Coins,
  Baby,
  Home,
  Shield,
  FileText,
  Sparkles,
  ArrowRight,
  CheckCircle,
  HelpCircle,
  Search,
  ExternalLink,
} from 'lucide-react';
import { api } from '../utils/api';
import { SchemeRecord } from '../types';
import { RecordCard } from '../components/RecordCard';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { useTranslation } from '../i18n';

const CATEGORY_ICONS: Record<string, React.ReactNode> = {
  'Education and Scholarships': <GraduationCap className="w-6 h-6 text-blue-600" />,
  'Agriculture and Farmers': <Tractor className="w-6 h-6 text-emerald-600" />,
  Healthcare: <HeartPulse className="w-6 h-6 text-rose-600" />,
  Employment: <Briefcase className="w-6 h-6 text-amber-600" />,
  'Financial Assistance': <Coins className="w-6 h-6 text-indigo-600" />,
  'Women and Child Welfare': <Baby className="w-6 h-6 text-pink-600" />,
  Housing: <Home className="w-6 h-6 text-teal-600" />,
  'Social Security': <Shield className="w-6 h-6 text-purple-600" />,
  'Other Citizen Services': <FileText className="w-6 h-6 text-slate-600" />,
};

export const Landing: React.FC = () => {
  const { t } = useTranslation();
  const { guestLogin } = useAuth();
  const navigate = useNavigate();
  const [featuredRecords, setFeaturedRecords] = useState<SchemeRecord[]>([]);
  const [loading, setLoading] = useState(true);

  const handleGuestTour = async () => {
    try {
      await guestLogin();
      navigate('/dashboard');
    } catch {
      navigate('/login');
    }
  };

  useEffect(() => {
    const fetchFeatured = async () => {
      try {
        const res = await api.records.list({ record_type: 'scheme' });
        setFeaturedRecords(res.records.slice(0, 4));
      } catch (err) {
        console.error('Failed to load featured records', err);
      } finally {
        setLoading(false);
      }
    };
    fetchFeatured();
  }, []);

  const categories = [
    { name: 'Education and Scholarships', label: t('categories.education') },
    { name: 'Agriculture and Farmers', label: t('categories.agriculture') },
    { name: 'Healthcare', label: t('categories.healthcare') },
    { name: 'Employment', label: t('categories.employment') },
    { name: 'Financial Assistance', label: t('categories.financial') },
    { name: 'Women and Child Welfare', label: t('categories.women_child') },
    { name: 'Housing', label: t('categories.housing') },
    { name: 'Social Security', label: t('categories.social_security') },
    { name: 'Other Citizen Services', label: t('categories.services') },
  ];

  return (
    <div>
      {/* Hero Section */}
      <section className="relative bg-gradient-to-b from-slate-900 via-slate-900 to-slate-800 text-white py-16 sm:py-24 px-4 sm:px-6 lg:px-8 overflow-hidden">
        <div className="absolute inset-0 opacity-10 bg-[radial-gradient(#3B82F6_1px,transparent_1px)] [background-size:16px_16px] pointer-events-none" />

        <div className="max-w-4xl mx-auto text-center relative z-10">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-500/10 border border-blue-400/30 text-blue-300 text-xs font-semibold mb-6">
            <Sparkles className="w-4 h-4 text-blue-400" />
            <span>Problem Statement #11 • GRAVITON 2026</span>
          </div>

          <h1 className="text-3xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white leading-tight">
            {t('hero.headline')}
          </h1>

          <p className="mt-5 text-base sm:text-lg text-slate-300 max-w-2xl mx-auto leading-relaxed">
            {t('hero.subtext')}
          </p>

          <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3">
            <button
              type="button"
              onClick={handleGuestTour}
              className="w-full sm:w-auto px-7 py-3.5 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-xl shadow-lg transition flex items-center justify-center gap-2 text-sm"
            >
              <Sparkles className="w-4 h-4 text-emerald-200" />
              <span>Explore as Guest (HR Demo)</span>
            </button>

            <Link
              to="/schemes"
              className="w-full sm:w-auto px-7 py-3.5 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-xl shadow-lg transition flex items-center justify-center gap-2 text-sm"
            >
              <Search className="w-4 h-4" />
              <span>{t('hero.cta_primary')}</span>
            </Link>

            <Link
              to="/assistant"
              className="w-full sm:w-auto px-7 py-3.5 bg-slate-800 hover:bg-slate-700 text-slate-100 border border-slate-700 font-semibold rounded-xl transition flex items-center justify-center gap-2 text-sm"
            >
              <Sparkles className="w-4 h-4 text-blue-400" />
              <span>{t('hero.cta_secondary')}</span>
            </Link>
          </div>

          {/* Quick Stats or Capabilities */}
          <div className="mt-12 pt-8 border-t border-slate-800/80 grid grid-cols-2 sm:grid-cols-4 gap-4 text-left">
            <div className="p-3 bg-slate-800/50 rounded-xl border border-slate-800">
              <span className="text-blue-400 font-bold text-sm block">1. Locate Services</span>
              <span className="text-slate-400 text-xs">Search 10+ welfare schemes & citizen services</span>
            </div>
            <div className="p-3 bg-slate-800/50 rounded-xl border border-slate-800">
              <span className="text-blue-400 font-bold text-sm block">2. Eligibility Engine</span>
              <span className="text-slate-400 text-xs">Transparent rule-by-rule evaluation</span>
            </div>
            <div className="p-3 bg-slate-800/50 rounded-xl border border-slate-800">
              <span className="text-blue-400 font-bold text-sm block">3. Document Checklists</span>
              <span className="text-slate-400 text-xs">Printable checklists with obtain guidance</span>
            </div>
            <div className="p-3 bg-slate-800/50 rounded-xl border border-slate-800">
              <span className="text-blue-400 font-bold text-sm block">4. Grounded Official URLs</span>
              <span className="text-slate-400 text-xs">Verified portals with direct citations</span>
            </div>
          </div>
        </div>
      </section>

      {/* Categories Grid */}
      <section className="py-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-10">
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            {t('categories.title')}
          </h2>
          <p className="text-sm text-slate-600 mt-2">
            Targeted services for students, farmers, rural families, and everyday citizens
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {categories.map((cat) => (
            <Link
              key={cat.name}
              to={`/schemes?category=${encodeURIComponent(cat.name)}`}
              className="p-5 bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-md hover:border-blue-300 transition flex items-center gap-4 group"
            >
              <div className="w-12 h-12 rounded-xl bg-slate-50 flex items-center justify-center shrink-0 group-hover:scale-105 transition">
                {CATEGORY_ICONS[cat.name] || <FileText className="w-6 h-6 text-slate-600" />}
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="text-sm font-semibold text-slate-900 group-hover:text-blue-700 transition truncate">
                  {cat.label}
                </h3>
                <span className="text-xs text-slate-500 mt-0.5 flex items-center gap-1">
                  View schemes <ArrowRight className="w-3 h-3 group-hover:translate-x-0.5 transition" />
                </span>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section className="py-14 bg-slate-100 border-y border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              {t('how_it_works.title')}
            </h2>
            <p className="text-sm text-slate-600 mt-2">
              Simple 3-step navigation designed for complete beginners and non-technical citizens
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
              <div className="w-10 h-10 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center font-bold text-base mb-4">
                1
              </div>
              <h3 className="text-base font-bold text-slate-900">{t('how_it_works.step1_title')}</h3>
              <p className="text-xs text-slate-600 mt-2 leading-relaxed">{t('how_it_works.step1_desc')}</p>
            </div>

            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
              <div className="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold text-base mb-4">
                2
              </div>
              <h3 className="text-base font-bold text-slate-900">{t('how_it_works.step2_title')}</h3>
              <p className="text-xs text-slate-600 mt-2 leading-relaxed">{t('how_it_works.step2_desc')}</p>
            </div>

            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
              <div className="w-10 h-10 rounded-xl bg-indigo-100 text-indigo-700 flex items-center justify-center font-bold text-base mb-4">
                3
              </div>
              <h3 className="text-base font-bold text-slate-900">{t('how_it_works.step3_title')}</h3>
              <p className="text-xs text-slate-600 mt-2 leading-relaxed">{t('how_it_works.step3_desc')}</p>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Verified Records */}
      <section className="py-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-8 flex-wrap gap-4">
          <div>
            <h2 className="text-2xl font-bold text-slate-900 tracking-tight">
              Featured Government Schemes
            </h2>
            <p className="text-xs text-slate-600 mt-1">
              Real verified schemes with official eligibility criteria and application links
            </p>
          </div>
          <Link
            to="/schemes"
            className="text-xs font-semibold text-blue-700 hover:text-blue-800 flex items-center gap-1"
          >
            <span>View All Schemes</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        {loading ? (
          <LoadingSpinner message="Loading schemes..." />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
            {featuredRecords.map((r) => (
              <RecordCard key={r.id} record={r} />
            ))}
          </div>
        )}
      </section>

      {/* Trust & Transparency */}
      <section className="py-14 bg-white border-t border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl mx-auto text-center mb-10">
            <h2 className="text-2xl font-bold text-slate-900 tracking-tight">
              {t('trust.title')}
            </h2>
            <p className="text-xs text-slate-600 mt-2">
              Built on strict data integrity principles. No invented criteria, no hallucinated benefits.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-5 bg-slate-50 border border-slate-200 rounded-2xl">
              <CheckCircle className="w-6 h-6 text-emerald-600 mb-3" />
              <h3 className="text-sm font-bold text-slate-900">{t('trust.point1_title')}</h3>
              <p className="text-xs text-slate-600 mt-2 leading-relaxed">{t('trust.point1_desc')}</p>
            </div>

            <div className="p-5 bg-slate-50 border border-slate-200 rounded-2xl">
              <HelpCircle className="w-6 h-6 text-blue-600 mb-3" />
              <h3 className="text-sm font-bold text-slate-900">{t('trust.point2_title')}</h3>
              <p className="text-xs text-slate-600 mt-2 leading-relaxed">{t('trust.point2_desc')}</p>
            </div>

            <div className="p-5 bg-slate-50 border border-slate-200 rounded-2xl">
              <Shield className="w-6 h-6 text-indigo-600 mb-3" />
              <h3 className="text-sm font-bold text-slate-900">{t('trust.point3_title')}</h3>
              <p className="text-xs text-slate-600 mt-2 leading-relaxed">{t('trust.point3_desc')}</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};
