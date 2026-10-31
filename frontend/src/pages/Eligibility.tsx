import React, { useEffect, useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { CheckCircle2, XCircle, HelpCircle, AlertCircle, ArrowRight, ShieldCheck } from 'lucide-react';
import { api } from '../utils/api';
import { EligibilityResult, SchemeRecord } from '../types';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorMessage } from '../components/ErrorMessage';
import { EligibilityBadge } from '../components/EligibilityBadge';
import { useAuth } from '../hooks/useAuth';
import { useTranslation } from '../i18n';

export const Eligibility: React.FC = () => {
  const { user } = useAuth();
  const { t } = useTranslation();
  const [searchParams] = useSearchParams();
  const initialRecordId = searchParams.get('record_id') || '';

  const [schemes, setSchemes] = useState<SchemeRecord[]>([]);
  const [selectedSchemeId, setSelectedSchemeId] = useState<string>(initialRecordId);

  // Form profile state
  const [age, setAge] = useState<string>('20');
  const [state, setState] = useState<string>('Punjab');
  const [incomeLakh, setIncomeLakh] = useState<string>('2.0');
  const [occupation, setOccupation] = useState<string>('student');
  const [category, setCategory] = useState<string>('SC');
  const [gender, setGender] = useState<string>('male');

  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<EligibilityResult[]>([]);
  const [error, setError] = useState<string | null>(null);

  // Pre-fill from user profile if available
  useEffect(() => {
    if (user?.profile_data) {
      const p = user.profile_data;
      if (p.age) setAge(String(p.age));
      if (p.state) setState(p.state);
      if (p.annual_family_income) setIncomeLakh(String(p.annual_family_income / 100000));
      if (p.occupation) setOccupation(p.occupation);
      if (p.category) setCategory(p.category);
      if (p.gender) setGender(p.gender);
    }
  }, [user]);

  // Load available schemes
  useEffect(() => {
    const loadSchemes = async () => {
      try {
        const res = await api.records.list({ record_type: 'scheme' });
        setSchemes(res.records);
      } catch (e) {
        console.error('Failed to load schemes', e);
      }
    };
    loadSchemes();
  }, []);

  const handleEvaluate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const numericAge = parseInt(age, 10);
    const numericIncome = Math.round(parseFloat(incomeLakh || '0') * 100000);

    const profileData = {
      age: isNaN(numericAge) ? undefined : numericAge,
      state: state || undefined,
      annual_family_income: isNaN(numericIncome) ? undefined : numericIncome,
      occupation: occupation || undefined,
      category: category || undefined,
      gender: gender || undefined,
    };

    try {
      if (selectedSchemeId) {
        // Single scheme check
        const res = await api.eligibility.check(selectedSchemeId, profileData);
        setResults([res]);
      } else {
        // Check all schemes
        const resList = await api.eligibility.checkAll(profileData);
        setResults(resList);
      }
    } catch (err: any) {
      setError(err.message || 'Eligibility evaluation failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Title */}
      <div className="mb-8 text-center max-w-2xl mx-auto">
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          {t('eligibility.title')}
        </h1>
        <p className="text-xs sm:text-sm text-slate-600 mt-2">
          {t('eligibility.subtitle')}
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Profile Inputs Card (5 cols) */}
        <div className="lg:col-span-5 bg-white p-6 rounded-3xl border border-slate-200 shadow-sm">
          <h2 className="text-sm font-bold text-slate-900 mb-4 pb-2 border-b border-slate-100">
            Citizen Details Form
          </h2>

          <form onSubmit={handleEvaluate} className="space-y-4">
            {/* Scheme Selector */}
            <div>
              <label className="text-xs font-semibold text-slate-700 block mb-1">
                Evaluate For Scheme
              </label>
              <select
                value={selectedSchemeId}
                onChange={(e) => setSelectedSchemeId(e.target.value)}
                className="w-full text-xs p-2.5 bg-slate-50 border border-slate-300 rounded-xl text-slate-900 focus:ring-2 focus:ring-blue-500 font-medium"
              >
                <option value="">Check All Schemes (Comprehensive Search)</option>
                {schemes.map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Age */}
            <div>
              <label className="text-xs font-semibold text-slate-700 block mb-1">
                {t('eligibility.age')}
              </label>
              <input
                type="number"
                min="0"
                max="120"
                value={age}
                onChange={(e) => setAge(e.target.value)}
                className="w-full text-xs p-2.5 bg-slate-50 border border-slate-300 rounded-xl"
                placeholder="e.g. 20"
                required
              />
            </div>

            {/* State */}
            <div>
              <label className="text-xs font-semibold text-slate-700 block mb-1">
                {t('eligibility.state')}
              </label>
              <select
                value={state}
                onChange={(e) => setState(e.target.value)}
                className="w-full text-xs p-2.5 bg-slate-50 border border-slate-300 rounded-xl"
              >
                <option value="Punjab">Punjab</option>
                <option value="Haryana">Haryana</option>
                <option value="Delhi">Delhi</option>
                <option value="Uttar Pradesh">Uttar Pradesh</option>
                <option value="Bihar">Bihar</option>
                <option value="Rajasthan">Rajasthan</option>
                <option value="Maharashtra">Maharashtra</option>
                <option value="Other">Other State</option>
              </select>
            </div>

            {/* Income in Lakhs */}
            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="text-xs font-semibold text-slate-700">
                  {t('eligibility.income_lakh')}
                </label>
                <span className="text-[11px] text-blue-700 font-medium">
                  = ₹{(parseFloat(incomeLakh || '0') * 100000).toLocaleString('en-IN')}
                </span>
              </div>
              <input
                type="number"
                step="0.1"
                min="0"
                max="100"
                value={incomeLakh}
                onChange={(e) => setIncomeLakh(e.target.value)}
                className="w-full text-xs p-2.5 bg-slate-50 border border-slate-300 rounded-xl"
                placeholder="e.g. 2.5"
                required
              />
            </div>

            {/* Occupation */}
            <div>
              <label className="text-xs font-semibold text-slate-700 block mb-1">
                {t('eligibility.occupation')}
              </label>
              <select
                value={occupation}
                onChange={(e) => setOccupation(e.target.value)}
                className="w-full text-xs p-2.5 bg-slate-50 border border-slate-300 rounded-xl"
              >
                <option value="student">Student</option>
                <option value="farmer">Farmer / Agricultural Worker</option>
                <option value="artisan">Artisan / Craftsperson</option>
                <option value="unorganized_worker">Unorganized Worker / Daily Wage</option>
                <option value="self_employed">Self Employed / Shopkeeper</option>
                <option value="unemployed">Unemployed</option>
                <option value="salaried">Salaried Employee</option>
              </select>
            </div>

            {/* Category */}
            <div>
              <label className="text-xs font-semibold text-slate-700 block mb-1">
                {t('eligibility.category')}
              </label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full text-xs p-2.5 bg-slate-50 border border-slate-300 rounded-xl"
              >
                <option value="SC">Scheduled Caste (SC)</option>
                <option value="ST">Scheduled Tribe (ST)</option>
                <option value="OBC">Other Backward Class (OBC)</option>
                <option value="General">General / EWS</option>
              </select>
            </div>

            {/* Gender */}
            <div>
              <label className="text-xs font-semibold text-slate-700 block mb-1">
                {t('eligibility.gender')}
              </label>
              <select
                value={gender}
                onChange={(e) => setGender(e.target.value)}
                className="w-full text-xs p-2.5 bg-slate-50 border border-slate-300 rounded-xl"
              >
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl text-xs shadow-md transition disabled:opacity-50 mt-2"
            >
              {loading ? 'Evaluating deterministic rules...' : t('eligibility.check_now')}
            </button>
          </form>
        </div>

        {/* Results Column (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          {error && <ErrorMessage message={error} />}

          {loading ? (
            <LoadingSpinner message="Checking statutory rules against your profile..." />
          ) : results.length === 0 ? (
            <div className="bg-white p-8 rounded-3xl border border-slate-200 text-center shadow-sm">
              <ShieldCheck className="w-12 h-12 text-blue-500 mx-auto mb-3 opacity-80" />
              <h3 className="text-base font-bold text-slate-800">Ready to Evaluate</h3>
              <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto leading-relaxed">
                Fill in your details on the left and click "{t('eligibility.check_now')}" to see transparent rule results.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center justify-between text-xs text-slate-500 px-1">
                <span>Evaluated <strong>{results.length}</strong> scheme(s)</span>
              </div>

              {results.map((res) => (
                <div
                  key={res.record_id}
                  className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm"
                >
                  {/* Scheme Header */}
                  <div className="flex items-start justify-between gap-3 pb-3 border-b border-slate-100 flex-wrap">
                    <div>
                      <h3 className="text-sm font-bold text-slate-900">{res.record_name}</h3>
                      <span className="text-[11px] text-slate-500">{res.category}</span>
                    </div>
                    <EligibilityBadge status={res.overall_status} />
                  </div>

                  {/* Summary Message */}
                  <p className="text-xs text-slate-700 mt-3 font-medium bg-slate-50 p-3 rounded-xl border border-slate-100">
                    {res.message}
                  </p>

                  {/* Rule-by-rule breakdown */}
                  {res.rule_results && res.rule_results.length > 0 && (
                    <div className="mt-4 space-y-2">
                      <span className="text-[11px] font-bold text-slate-700 uppercase tracking-wider block mb-1">
                        Audited Rule Breakdown:
                      </span>
                      {res.rule_results.map((rule, idx) => (
                        <div
                          key={idx}
                          className={`p-3 rounded-xl border text-xs flex items-start gap-2.5 ${
                            rule.status === 'MET'
                              ? 'bg-emerald-50/50 border-emerald-200 text-emerald-950'
                              : rule.status === 'NOT_MET'
                              ? 'bg-red-50/50 border-red-200 text-red-950'
                              : 'bg-amber-50/50 border-amber-200 text-amber-950'
                          }`}
                        >
                          {rule.status === 'MET' ? (
                            <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                          ) : rule.status === 'NOT_MET' ? (
                            <XCircle className="w-4 h-4 text-red-600 shrink-0 mt-0.5" />
                          ) : (
                            <HelpCircle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                          )}

                          <div className="flex-1 min-w-0">
                            <div className="flex items-center justify-between gap-2">
                              <span className="font-semibold">{rule.description}</span>
                              <span
                                className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
                                  rule.status === 'MET'
                                    ? 'bg-emerald-100 text-emerald-800'
                                    : rule.status === 'NOT_MET'
                                    ? 'bg-red-100 text-red-800'
                                    : 'bg-amber-100 text-amber-800'
                                }`}
                              >
                                {rule.status}
                              </span>
                            </div>

                            {rule.source_excerpt && (
                              <p className="text-[11px] text-slate-500 italic mt-1">
                                Source excerpt: "{rule.source_excerpt}"
                              </p>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Actions */}
                  <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between gap-2">
                    <Link
                      to={`/checklist/${res.record_id}`}
                      className="text-xs text-blue-700 font-semibold hover:underline"
                    >
                      Prepare document checklist →
                    </Link>

                    <Link
                      to={`/schemes/${res.record_id}`}
                      className="text-xs text-slate-600 hover:text-slate-900"
                    >
                      Scheme details
                    </Link>
                  </div>
                </div>
              ))}

              {/* Disclaimer */}
              <div className="p-4 bg-slate-100 border border-slate-200 rounded-2xl text-[11px] text-slate-600 flex items-start gap-2">
                <AlertCircle className="w-4 h-4 text-slate-500 shrink-0 mt-0.5" />
                <p>{t('eligibility.disclaimer')}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
