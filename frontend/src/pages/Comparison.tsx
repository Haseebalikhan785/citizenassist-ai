import React, { useEffect, useState } from 'react';
import { Plus, X, ExternalLink, ArrowRight, Layers } from 'lucide-react';
import { api } from '../utils/api';
import { SchemeRecord } from '../types';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { DemoBadge } from '../components/DemoBadge';

export const Comparison: React.FC = () => {
  const [allSchemes, setAllSchemes] = useState<SchemeRecord[]>([]);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAll = async () => {
      try {
        const res = await api.records.list({ record_type: 'scheme' });
        setAllSchemes(res.records);
        // Default select top 2 schemes
        if (res.records.length >= 2) {
          setSelectedIds([res.records[0].id, res.records[1].id]);
        }
      } catch (e) {
        console.error('Failed to load comparison schemes', e);
      } finally {
        setLoading(false);
      }
    };
    fetchAll();
  }, []);

  const addScheme = (id: string) => {
    if (id && !selectedIds.includes(id) && selectedIds.length < 3) {
      setSelectedIds([...selectedIds, id]);
    }
  };

  const removeScheme = (id: string) => {
    setSelectedIds(selectedIds.filter((item) => item !== id));
  };

  if (loading) return <LoadingSpinner message="Loading comparison matrix..." />;

  const comparedSchemes = selectedIds
    .map((id) => allSchemes.find((s) => s.id === id))
    .filter(Boolean) as SchemeRecord[];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
          <Layers className="w-7 h-7 text-blue-600" />
          Scheme Side-by-Side Comparison
        </h1>
        <p className="text-xs sm:text-sm text-slate-600 mt-1">
          Compare up to 3 welfare schemes side-by-side to understand differences in eligibility, benefits, and required documents.
        </p>
      </div>

      {/* Scheme Pickers Header */}
      <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-sm mb-6 flex flex-wrap items-center justify-between gap-4">
        <span className="text-xs font-bold text-slate-700">
          Comparing {comparedSchemes.length} of 3 Schemes
        </span>

        {selectedIds.length < 3 && (
          <div className="flex items-center gap-2">
            <select
              onChange={(e) => {
                addScheme(e.target.value);
                e.target.value = '';
              }}
              defaultValue=""
              className="text-xs p-2 bg-slate-50 border border-slate-300 rounded-xl font-medium text-slate-800"
            >
              <option value="" disabled>
                + Add another scheme to compare...
              </option>
              {allSchemes
                .filter((s) => !selectedIds.includes(s.id))
                .map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.name}
                  </option>
                ))}
            </select>
          </div>
        )}
      </div>

      {comparedSchemes.length === 0 ? (
        <div className="p-8 bg-white rounded-3xl border border-slate-200 text-center shadow-sm">
          <p className="text-sm text-slate-600">Please select at least one scheme to compare.</p>
        </div>
      ) : (
        <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-x-auto">
          <table className="w-full text-xs text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50/70">
                <th className="p-4 w-44 font-bold text-slate-500 uppercase tracking-wider text-[11px]">
                  Scheme Details
                </th>
                {comparedSchemes.map((s) => (
                  <th key={s.id} className="p-4 min-w-[260px] align-top">
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex-1">
                        <span className="text-[10px] font-semibold text-blue-700 bg-blue-50 px-2 py-0.5 rounded-full block w-fit mb-1">
                          {s.category}
                        </span>
                        <h3 className="text-sm font-bold text-slate-900 leading-snug">{s.name}</h3>
                      </div>
                      <button
                        onClick={() => removeScheme(s.id)}
                        className="p-1 text-slate-400 hover:text-red-500 rounded-lg hover:bg-slate-100"
                        title="Remove scheme"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                  </th>
                ))}
              </tr>
            </thead>

            <tbody className="divide-y divide-slate-100">
              {/* Row: Verification */}
              <tr>
                <td className="p-4 font-bold text-slate-700 bg-slate-50/50">Status</td>
                {comparedSchemes.map((s) => (
                  <td key={s.id} className="p-4">
                    <DemoBadge status={s.verification_status} />
                  </td>
                ))}
              </tr>

              {/* Row: Benefits */}
              <tr>
                <td className="p-4 font-bold text-slate-700 bg-slate-50/50">Benefits</td>
                {comparedSchemes.map((s) => (
                  <td key={s.id} className="p-4 text-slate-800 leading-relaxed font-medium">
                    {s.benefits || 'Not explicitly stated'}
                  </td>
                ))}
              </tr>

              {/* Row: Target Beneficiaries */}
              <tr>
                <td className="p-4 font-bold text-slate-700 bg-slate-50/50">Beneficiaries</td>
                {comparedSchemes.map((s) => (
                  <td key={s.id} className="p-4 text-slate-700 capitalize">
                    {s.target_beneficiaries?.join(', ') || 'General Public'}
                  </td>
                ))}
              </tr>

              {/* Row: Income Limit */}
              <tr>
                <td className="p-4 font-bold text-slate-700 bg-slate-50/50">Income Limit</td>
                {comparedSchemes.map((s) => (
                  <td key={s.id} className="p-4 text-slate-700 font-semibold">
                    {s.income_criteria?.max_annual
                      ? `Up to ₹${s.income_criteria.max_annual.toLocaleString('en-IN')} / year`
                      : 'No strict limit'}
                  </td>
                ))}
              </tr>

              {/* Row: Required Documents */}
              <tr>
                <td className="p-4 font-bold text-slate-700 bg-slate-50/50">Documents</td>
                {comparedSchemes.map((s) => (
                  <td key={s.id} className="p-4 text-slate-700">
                    <ul className="list-disc pl-4 space-y-1">
                      {s.required_documents?.map((d, i) => (
                        <li key={i}>{typeof d === 'string' ? d : d.name}</li>
                      ))}
                    </ul>
                  </td>
                ))}
              </tr>

              {/* Row: Official Link */}
              <tr>
                <td className="p-4 font-bold text-slate-700 bg-slate-50/50">Official Link</td>
                {comparedSchemes.map((s) => (
                  <td key={s.id} className="p-4">
                    {s.application_url && (
                      <a
                        href={s.application_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1 text-blue-700 font-semibold hover:underline"
                      >
                        <span>Official Portal</span>
                        <ExternalLink className="w-3.5 h-3.5" />
                      </a>
                    )}
                  </td>
                ))}
              </tr>
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
