import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  Building2,
  ExternalLink,
  CheckSquare,
  Sparkles,
  Bookmark,
  Share2,
  ShieldCheck,
  CheckCircle,
  HelpCircle,
  AlertTriangle,
  FileText,
  Clock,
  ArrowLeft,
} from 'lucide-react';
import { api } from '../utils/api';
import { SchemeRecord } from '../types';
import { DemoBadge } from '../components/DemoBadge';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorMessage } from '../components/ErrorMessage';
import { useAuth } from '../hooks/useAuth';
import { useTranslation } from '../i18n';

export const SchemeDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { user } = useAuth();
  const { language, t } = useTranslation();

  const [record, setRecord] = useState<SchemeRecord | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isSaved, setIsSaved] = useState(false);
  const [saveLoading, setSaveLoading] = useState(false);
  const [feedbackOpen, setFeedbackOpen] = useState(false);
  const [feedbackType, setFeedbackType] = useState('incorrect_info');
  const [feedbackText, setFeedbackText] = useState('');
  const [feedbackSuccess, setFeedbackSuccess] = useState(false);

  useEffect(() => {
    if (!id) return;
    const fetchDetail = async () => {
      setLoading(true);
      setError(null);
      try {
        const rec = await api.records.get(id);
        setRecord(rec);
      } catch (err: any) {
        setError(err.message || 'Scheme not found');
      } finally {
        setLoading(false);
      }
    };
    fetchDetail();
  }, [id]);

  const handleSaveToggle = async () => {
    if (!id || !user) return;
    setSaveLoading(true);
    try {
      if (isSaved) {
        await api.saved.remove(id);
        setIsSaved(false);
      } else {
        await api.saved.save(id);
        setIsSaved(true);
      }
    } catch (e) {
      console.error('Failed to toggle save', e);
    } finally {
      setSaveLoading(false);
    }
  };

  const handleFeedbackSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!id || !feedbackText.trim()) return;
    try {
      await api.feedback.submit({
        record_id: id,
        feedback_type: feedbackType,
        description: feedbackText.trim(),
      });
      setFeedbackSuccess(true);
      setTimeout(() => {
        setFeedbackOpen(false);
        setFeedbackSuccess(false);
        setFeedbackText('');
      }, 2000);
    } catch (e) {
      console.error('Failed to submit feedback', e);
    }
  };

  if (loading) return <LoadingSpinner message="Loading scheme details..." />;
  if (error || !record) return <ErrorMessage message={error || 'Scheme not found'} />;

  const displayName =
    language === 'hi' && record.name_hi
      ? record.name_hi
      : language === 'pa' && record.name_pa
      ? record.name_pa
      : record.name;

  const displayDesc =
    language === 'hi' && record.description_hi
      ? record.description_hi
      : language === 'pa' && record.description_pa
      ? record.description_pa
      : record.description;

  const displayBenefits =
    language === 'hi' && record.benefits_hi
      ? record.benefits_hi
      : language === 'pa' && record.benefits_pa
      ? record.benefits_pa
      : record.benefits;

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Back button */}
      <Link
        to="/schemes"
        className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-800 mb-4 transition"
      >
        <ArrowLeft className="w-4 h-4" /> Back to all schemes
      </Link>

      {/* Main Card */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden p-6 sm:p-8">
        {/* Header section */}
        <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-6 border-b border-slate-100">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2 flex-wrap">
              <span className="px-3 py-1 rounded-full text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200">
                {record.category || 'General'}
              </span>
              <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-700 capitalize">
                {record.level || 'Central'} Level
              </span>
              <DemoBadge status={record.verification_status} />
            </div>

            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 leading-tight">
              {displayName}
            </h1>

            {record.department && (
              <p className="text-xs sm:text-sm text-slate-500 mt-2 flex items-center gap-1.5">
                <Building2 className="w-4 h-4 text-slate-400" />
                {record.department}
              </p>
            )}
          </div>

          {/* Top Actions */}
          <div className="flex items-center gap-2 shrink-0">
            {user && (
              <button
                onClick={handleSaveToggle}
                disabled={saveLoading}
                className={`p-2.5 rounded-xl border transition flex items-center gap-1 text-xs font-medium ${
                  isSaved
                    ? 'bg-blue-50 text-blue-700 border-blue-300'
                    : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
                }`}
                title={isSaved ? 'Remove from saved' : 'Save scheme'}
              >
                <Bookmark className={`w-4 h-4 ${isSaved ? 'fill-blue-600' : ''}`} />
                <span>{isSaved ? 'Saved' : 'Save'}</span>
              </button>
            )}

            <button
              onClick={() => {
                navigator.clipboard.writeText(window.location.href);
                alert('Scheme link copied to clipboard!');
              }}
              className="p-2.5 rounded-xl border border-slate-200 text-slate-600 hover:bg-slate-50 transition"
              title="Share link"
            >
              <Share2 className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Primary CTA Row */}
        <div className="my-6 p-4 sm:p-5 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-2xl flex flex-col sm:flex-row items-center justify-between gap-4">
          <div>
            <span className="text-xs font-bold text-blue-900 block">Ready to apply or check requirements?</span>
            <span className="text-xs text-blue-700 mt-0.5 block">
              Test your exact eligibility or build a personalized document checklist.
            </span>
          </div>

          <div className="flex items-center gap-2.5 w-full sm:w-auto">
            <Link
              to={`/eligibility?record_id=${record.id}`}
              className="flex-1 sm:flex-initial px-4 py-2.5 bg-blue-700 hover:bg-blue-800 text-white text-xs font-semibold rounded-xl shadow-sm transition text-center"
            >
              {t('record.check_eligibility')}
            </Link>

            <Link
              to={`/checklist/${record.id}`}
              className="flex-1 sm:flex-initial px-4 py-2.5 bg-white hover:bg-slate-50 text-blue-700 border border-blue-300 text-xs font-semibold rounded-xl shadow-sm transition flex items-center justify-center gap-1.5"
            >
              <CheckSquare className="w-4 h-4" />
              <span>{t('record.open_checklist')}</span>
            </Link>
          </div>
        </div>

        {/* Sections */}
        <div className="space-y-8 mt-6">
          {/* Description */}
          <div>
            <h2 className="text-base font-bold text-slate-900 mb-2">About the Scheme</h2>
            <p className="text-sm text-slate-700 leading-relaxed">{displayDesc}</p>
          </div>

          {/* Benefits */}
          {displayBenefits && (
            <div className="p-5 bg-emerald-50/70 border border-emerald-200 rounded-2xl">
              <h2 className="text-sm font-bold text-emerald-950 mb-1.5 flex items-center gap-1.5">
                <CheckCircle className="w-4 h-4 text-emerald-700" /> Key Benefits & Entitlements
              </h2>
              <p className="text-xs sm:text-sm text-emerald-900 leading-relaxed font-medium">
                {displayBenefits}
              </p>
            </div>
          )}

          {/* Eligibility Criteria */}
          <div>
            <h2 className="text-base font-bold text-slate-900 mb-3">Eligibility Criteria</h2>
            <div className="space-y-3">
              {record.other_conditions && record.other_conditions.length > 0 ? (
                <ul className="space-y-2">
                  {record.other_conditions.map((cond, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-xs sm:text-sm text-slate-700">
                      <span className="w-1.5 h-1.5 rounded-full bg-blue-600 mt-2 shrink-0" />
                      <span>{cond}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-xs text-slate-500 italic">
                  Not stated in source — confirm on the official portal.
                </p>
              )}

              {/* Structured criteria cards */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-4">
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 text-xs">
                  <span className="text-slate-500 block">Applicable States</span>
                  <span className="font-semibold text-slate-800 mt-0.5 block">
                    {record.state_applicability?.join(', ') || 'All India'}
                  </span>
                </div>

                <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 text-xs">
                  <span className="text-slate-500 block">Target Beneficiaries</span>
                  <span className="font-semibold text-slate-800 mt-0.5 block">
                    {record.target_beneficiaries?.join(', ') || 'General Public'}
                  </span>
                </div>

                <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 text-xs">
                  <span className="text-slate-500 block">Income Limit</span>
                  <span className="font-semibold text-slate-800 mt-0.5 block">
                    {record.income_criteria?.max_annual
                      ? `Up to ₹${record.income_criteria.max_annual.toLocaleString('en-IN')}/year`
                      : 'No strict numerical limit'}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Required Documents */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-base font-bold text-slate-900">Required Documents</h2>
              <Link
                to={`/checklist/${record.id}`}
                className="text-xs font-semibold text-blue-600 hover:underline flex items-center gap-1"
              >
                <span>Interactive checklist</span>
                <CheckSquare className="w-3.5 h-3.5" />
              </Link>
            </div>

            {record.required_documents && record.required_documents.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {record.required_documents.map((doc, idx) => {
                  const docName = typeof doc === 'string' ? doc : doc.name;
                  const docDesc = typeof doc === 'string' ? '' : doc.description;
                  const linkedId = typeof doc === 'string' ? null : doc.linked_service_id;

                  return (
                    <div key={idx} className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl text-xs">
                      <div className="flex items-center justify-between gap-1">
                        <span className="font-bold text-slate-900">{docName}</span>
                        {linkedId && (
                          <Link
                            to={`/schemes/${linkedId}`}
                            className="text-[10px] bg-blue-100 text-blue-800 px-2 py-0.5 rounded font-semibold hover:bg-blue-200 transition"
                          >
                            How to get
                          </Link>
                        )}
                      </div>
                      {docDesc && <p className="text-slate-600 mt-1 leading-snug">{docDesc}</p>}
                    </div>
                  );
                })}
              </div>
            ) : (
              <p className="text-xs text-slate-500 italic">No specific documents specified.</p>
            )}
          </div>

          {/* Application Procedure */}
          {record.application_procedure && (
            <div>
              <h2 className="text-base font-bold text-slate-900 mb-2">How to Apply</h2>
              <div className="p-4 bg-slate-50 border border-slate-200 rounded-2xl text-xs sm:text-sm text-slate-700 leading-relaxed whitespace-pre-line">
                {record.application_procedure}
              </div>
            </div>
          )}

          {/* Official Verification Box */}
          <div className="p-5 bg-slate-100/80 border border-slate-200 rounded-2xl">
            <div className="flex items-center justify-between mb-2 flex-wrap gap-2">
              <span className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                <ShieldCheck className="w-4 h-4 text-blue-600" />
                Data Integrity & Source Verification
              </span>
              {record.last_verified_date && (
                <span className="text-[11px] text-slate-500 flex items-center gap-1">
                  <Clock className="w-3 h-3" /> Last verified: {record.last_verified_date}
                </span>
              )}
            </div>

            {record.source_excerpt && (
              <blockquote className="text-xs text-slate-600 italic bg-white p-3 rounded-xl border border-slate-200 my-2">
                "{record.source_excerpt}"
              </blockquote>
            )}

            <div className="flex items-center justify-between gap-3 mt-3 flex-wrap text-xs">
              <div className="flex items-center gap-3">
                {record.official_source_url && (
                  <a
                    href={record.official_source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-700 hover:underline flex items-center gap-1 font-semibold"
                  >
                    <span>Official Portal</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                )}
                {record.application_url && record.application_url !== record.official_source_url && (
                  <a
                    href={record.application_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-indigo-700 hover:underline flex items-center gap-1 font-semibold"
                  >
                    <span>Apply Online</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                )}
              </div>

              <button
                onClick={() => setFeedbackOpen(true)}
                className="text-[11px] text-slate-500 hover:text-slate-800 underline"
              >
                Report incorrect information
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Feedback Modal */}
      {feedbackOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-xl border border-slate-200">
            <h3 className="text-base font-bold text-slate-900 mb-1">Report Data Issue</h3>
            <p className="text-xs text-slate-600 mb-4">
              Help us maintain government data integrity by reporting outdated or inaccurate facts.
            </p>

            {feedbackSuccess ? (
              <div className="p-4 bg-emerald-50 text-emerald-800 rounded-xl text-xs text-center font-semibold">
                Thank you! Your feedback has been logged for admin review.
              </div>
            ) : (
              <form onSubmit={handleFeedbackSubmit} className="space-y-3">
                <div>
                  <label className="text-xs font-semibold text-slate-700 block mb-1">Issue Type</label>
                  <select
                    value={feedbackType}
                    onChange={(e) => setFeedbackType(e.target.value)}
                    className="w-full text-xs p-2 border border-slate-300 rounded-lg"
                  >
                    <option value="incorrect_info">Incorrect Criteria or Amount</option>
                    <option value="broken_link">Broken / Changed Official URL</option>
                    <option value="missing_info">Missing Document or Deadline</option>
                    <option value="other">Other Concern</option>
                  </select>
                </div>

                <div>
                  <label className="text-xs font-semibold text-slate-700 block mb-1">Description</label>
                  <textarea
                    rows={3}
                    value={feedbackText}
                    onChange={(e) => setFeedbackText(e.target.value)}
                    placeholder="Provide details or official source URL..."
                    className="w-full text-xs p-2.5 border border-slate-300 rounded-lg"
                    required
                  />
                </div>

                <div className="flex justify-end gap-2 pt-2">
                  <button
                    type="button"
                    onClick={() => setFeedbackOpen(false)}
                    className="px-3 py-1.5 text-xs text-slate-600 hover:bg-slate-100 rounded-lg"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-1.5 bg-blue-600 text-white text-xs font-semibold rounded-lg hover:bg-blue-700"
                  >
                    Submit Report
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
