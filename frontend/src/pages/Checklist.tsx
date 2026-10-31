import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Printer, CheckSquare, Square, AlertCircle, ArrowLeft, ExternalLink, ShieldAlert } from 'lucide-react';
import { api } from '../utils/api';
import { ChecklistItem, SchemeRecord } from '../types';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorMessage } from '../components/ErrorMessage';
import { useAuth } from '../hooks/useAuth';
import { useTranslation } from '../i18n';

export const Checklist: React.FC = () => {
  const { recordId } = useParams<{ recordId: string }>();
  const { user } = useAuth();
  const { t } = useTranslation();

  const [scheme, setScheme] = useState<SchemeRecord | null>(null);
  const [items, setItems] = useState<ChecklistItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!recordId) return;

    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const [rec, checkRes] = await Promise.all([
          api.records.get(recordId),
          api.checklist.get(recordId),
        ]);
        setScheme(rec);

        // Map checklist items with linked service info if available
        const rawDocs = rec.required_documents || [];
        const linkedMap: Record<string, string | null> = {};
        for (const rd of rawDocs) {
          if (typeof rd === 'object' && rd.name) {
            linkedMap[rd.name] = rd.linked_service_id || null;
          }
        }

        const enriched = checkRes.items.map((item) => ({
          ...item,
          linked_service_id: linkedMap[item.document_name] || null,
        }));
        setItems(enriched);
      } catch (err: any) {
        setError(err.message || 'Failed to load checklist');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [recordId]);

  const handleToggle = async (index: number) => {
    const item = items[index];
    const newStatus = !item.is_available;

    const nextItems = [...items];
    nextItems[index] = { ...item, is_available: newStatus };
    setItems(nextItems);

    if (user && recordId) {
      try {
        await api.checklist.update(recordId, item.document_name, newStatus);
      } catch (e) {
        console.error('Failed to sync checklist to backend', e);
      }
    }
  };

  const handlePrint = () => {
    window.print();
  };

  if (loading) return <LoadingSpinner message="Loading document checklist..." />;
  if (error || !scheme) return <ErrorMessage message={error || 'Scheme not found'} />;

  const readyCount = items.filter((i) => i.is_available).length;
  const totalCount = items.length;
  const progressPercent = totalCount > 0 ? Math.round((readyCount / totalCount) * 100) : 0;

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Non-print Back Navigation & Actions */}
      <div className="print:hidden flex items-center justify-between mb-6 flex-wrap gap-4">
        <Link
          to={`/schemes/${scheme.id}`}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-800 transition"
        >
          <ArrowLeft className="w-4 h-4" /> Back to {scheme.name}
        </Link>

        <button
          onClick={handlePrint}
          className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold rounded-xl shadow-sm transition flex items-center gap-2"
        >
          <Printer className="w-4 h-4" />
          <span>{t('checklist.print_button')}</span>
        </button>
      </div>

      {/* Main Checklist Card */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 sm:p-8 print:border-none print:shadow-none print:p-0">
        {/* Header */}
        <div className="border-b border-slate-100 pb-5">
          <div className="flex items-center gap-2 text-xs font-semibold text-blue-700 mb-1">
            <CheckSquare className="w-4 h-4" />
            <span>Document Readiness Checklist</span>
          </div>
          <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900">
            {scheme.name}
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Official department: {scheme.department || 'Government of India'}
          </p>
        </div>

        {/* Progress Bar (print:hidden) */}
        <div className="my-6 print:hidden">
          <div className="flex items-center justify-between text-xs mb-2">
            <span className="font-bold text-slate-800">
              {t('checklist.ready_count', { ready: readyCount, total: totalCount })}
            </span>
            <span className="font-semibold text-blue-700">{progressPercent}% Ready</span>
          </div>
          <div className="w-full h-3 bg-slate-100 rounded-full overflow-hidden border border-slate-200">
            <div
              className="h-full bg-blue-600 transition-all duration-300 rounded-full"
              style={{ width: `${progressPercent}%` }}
            />
          </div>

          {!user && (
            <p className="text-[11px] text-slate-500 mt-2 italic">
              Note: Login or create an account to save your checklist progress automatically across devices.
            </p>
          )}
        </div>

        {/* Printable list */}
        <div className="space-y-3 mt-6">
          <h2 className="text-sm font-bold text-slate-900 mb-2">Required Documents</h2>

          {items.length === 0 ? (
            <p className="text-xs text-slate-500 italic">No specific documents specified in the official source.</p>
          ) : (
            items.map((item, idx) => (
              <div
                key={idx}
                className={`p-4 rounded-2xl border transition ${
                  item.is_available
                    ? 'bg-emerald-50/40 border-emerald-200'
                    : 'bg-slate-50 border-slate-200'
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <button
                    type="button"
                    onClick={() => handleToggle(idx)}
                    className="flex items-start gap-3 text-left flex-1 group"
                  >
                    <div className="mt-0.5 text-blue-600">
                      {item.is_available ? (
                        <CheckSquare className="w-5 h-5 text-emerald-600" />
                      ) : (
                        <Square className="w-5 h-5 text-slate-400 group-hover:text-slate-600" />
                      )}
                    </div>

                    <div>
                      <span
                        className={`text-sm font-bold block ${
                          item.is_available ? 'text-emerald-950 line-through opacity-80' : 'text-slate-900'
                        }`}
                      >
                        {item.document_name}
                      </span>
                      <span className="text-xs text-slate-500 block mt-0.5">
                        {item.is_available ? 'Document marked as available' : 'Missing — needs to be arranged'}
                      </span>
                    </div>
                  </button>

                  {/* If linked to a service */}
                  {item.linked_service_id && (
                    <div className="shrink-0 text-right print:hidden">
                      <Link
                        to={`/schemes/${item.linked_service_id}`}
                        className="inline-flex items-center gap-1 text-[11px] font-semibold text-blue-700 bg-blue-100 hover:bg-blue-200 px-2.5 py-1 rounded-lg transition"
                      >
                        <span>Where to obtain</span>
                        <ExternalLink className="w-3 h-3" />
                      </Link>
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
        </div>

        {/* Application Link in Print and UI */}
        {scheme.application_url && (
          <div className="mt-8 pt-6 border-t border-slate-100 flex items-center justify-between gap-4 flex-wrap">
            <div>
              <span className="text-xs font-bold text-slate-800 block">Official Application Portal:</span>
              <span className="text-xs text-blue-700 underline break-all">{scheme.application_url}</span>
            </div>

            <a
              href={scheme.application_url}
              target="_blank"
              rel="noopener noreferrer"
              className="print:hidden px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-xl shadow-sm transition inline-flex items-center gap-1"
            >
              <span>Go to Official Portal</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>
        )}

        {/* Print Footer */}
        <div className="mt-8 pt-4 border-t border-slate-200 text-[10px] text-slate-400 text-center">
          CitizenAssist AI • Document Preparation Checklist • Always verify statutory rules on official portals.
        </div>
      </div>
    </div>
  );
};
