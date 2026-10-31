import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  User,
  Bookmark,
  CheckSquare,
  Sparkles,
  ExternalLink,
  ArrowRight,
  ShieldCheck,
  Search,
} from 'lucide-react';
import { api } from '../utils/api';
import { SavedItem, SchemeRecord, User as UserType } from '../types';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorMessage } from '../components/ErrorMessage';
import { useAuth } from '../hooks/useAuth';
import { useTranslation } from '../i18n';

export const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const { t } = useTranslation();

  const [savedItems, setSavedItems] = useState<SavedItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadSaved = async () => {
      try {
        const items = await api.saved.list();
        setSavedItems(items);
      } catch (err: any) {
        setError(err.message || 'Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };
    loadSaved();
  }, []);

  if (loading) return <LoadingSpinner message="Loading your personal dashboard..." />;

  const profileCompletion = user?.profile_data
    ? Math.round(
        (Object.keys(user.profile_data).filter((k) => user.profile_data[k] !== undefined).length /
          6) *
          100
      )
    : 0;

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-slate-900 to-blue-900 text-white rounded-3xl p-6 sm:p-8 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-6">
        <div>
          <span className="text-xs font-semibold text-blue-300 block mb-1">
            Citizen Navigator Dashboard
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            Welcome back, {user?.full_name || user?.email.split('@')[0]}
          </h1>
          <p className="text-xs sm:text-sm text-slate-300 mt-2 max-w-lg leading-relaxed">
            Track your bookmarked schemes, document preparation checklists, and personalized eligibility recommendations.
          </p>
        </div>

        <div className="bg-white/10 backdrop-blur-sm border border-white/20 p-4 rounded-2xl text-center shrink-0 w-full sm:w-48">
          <span className="text-[11px] text-slate-300 block">Profile Completion</span>
          <span className="text-2xl font-bold text-white block my-0.5">{profileCompletion}%</span>
          <Link
            to="/profile"
            className="text-[11px] text-blue-300 hover:text-white underline font-semibold"
          >
            Update details →
          </Link>
        </div>
      </div>

      {/* Quick Action Shortcuts */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <Link
          to="/assistant"
          className="p-4 bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition flex items-center gap-3.5 group"
        >
          <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center shrink-0 group-hover:bg-blue-600 group-hover:text-white transition">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900">Ask Assistant</h3>
            <p className="text-xs text-slate-500 mt-0.5">Natural language scheme discovery</p>
          </div>
        </Link>

        <Link
          to="/eligibility"
          className="p-4 bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition flex items-center gap-3.5 group"
        >
          <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center shrink-0 group-hover:bg-emerald-600 group-hover:text-white transition">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900">Check Eligibility</h3>
            <p className="text-xs text-slate-500 mt-0.5">Deterministic rule evaluation</p>
          </div>
        </Link>

        <Link
          to="/schemes"
          className="p-4 bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition flex items-center gap-3.5 group"
        >
          <div className="w-10 h-10 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center shrink-0 group-hover:bg-purple-600 group-hover:text-white transition">
            <Search className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900">All Schemes</h3>
            <p className="text-xs text-slate-500 mt-0.5">Browse 14 verified records</p>
          </div>
        </Link>
      </div>

      {/* Saved Schemes with Readiness View */}
      <section>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <Bookmark className="w-5 h-5 text-blue-600" />
            Saved Schemes & Readiness View
          </h2>
          <span className="text-xs text-slate-500">{savedItems.length} saved</span>
        </div>

        {savedItems.length === 0 ? (
          <div className="p-8 bg-white rounded-3xl border border-slate-200 text-center shadow-sm">
            <Bookmark className="w-10 h-10 text-slate-300 mx-auto mb-2" />
            <h3 className="text-sm font-bold text-slate-700">No saved schemes yet</h3>
            <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
              Browse through government schemes and click "Save" to build your personalized application tracker.
            </p>
            <Link
              to="/schemes"
              className="mt-4 inline-block px-4 py-2 bg-blue-600 text-white text-xs font-semibold rounded-xl hover:bg-blue-700 transition"
            >
              Browse Schemes
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {savedItems.map((item) => {
              const rec = item.record;
              if (!rec) return null;

              return (
                <div
                  key={item.id}
                  className="p-5 bg-white rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center justify-between gap-2 mb-2">
                      <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-blue-50 text-blue-700">
                        {rec.category}
                      </span>
                      <span className="text-[11px] text-slate-400">
                        Saved: {item.created_at?.split('T')[0] || 'Recently'}
                      </span>
                    </div>

                    <h3 className="text-sm font-bold text-slate-900 mb-1 leading-snug">
                      <Link to={`/schemes/${rec.id}`} className="hover:text-blue-700">
                        {rec.name}
                      </Link>
                    </h3>

                    <p className="text-xs text-slate-600 line-clamp-2 mt-1">{rec.description}</p>
                  </div>

                  {/* Readiness View Pill */}
                  <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between gap-2 text-xs">
                    <Link
                      to={`/checklist/${rec.id}`}
                      className="text-blue-700 hover:underline font-semibold flex items-center gap-1"
                    >
                      <CheckSquare className="w-3.5 h-3.5" />
                      <span>Checklist</span>
                    </Link>

                    {rec.application_url && (
                      <a
                        href={rec.application_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-slate-600 hover:text-slate-900 flex items-center gap-1"
                      >
                        <span>Apply</span>
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </section>
    </div>
  );
};
