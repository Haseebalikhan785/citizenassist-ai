import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, CheckSquare, ShieldAlert, Sparkles, Building2 } from 'lucide-react';
import { SchemeRecord } from '../types';
import { DemoBadge } from './DemoBadge';
import { useTranslation } from '../i18n';

export const RecordCard: React.FC<{ record: SchemeRecord; onSaveToggle?: () => void; isSaved?: boolean }> = ({
  record,
}) => {
  const { language, t } = useTranslation();

  // Pick localized title and description
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

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition flex flex-col p-5 group">
      {/* Badges row */}
      <div className="flex items-center justify-between gap-2 mb-3 flex-wrap">
        <div className="flex items-center gap-1.5 flex-wrap">
          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200">
            {record.category || 'General'}
          </span>
          <span className={`px-2 py-0.5 rounded-full text-[11px] font-medium ${
            record.record_type === 'scheme' ? 'bg-indigo-50 text-indigo-700' : 'bg-teal-50 text-teal-700'
          }`}>
            {record.record_type === 'scheme' ? t('record.scheme') : t('record.service')}
          </span>
        </div>
        <DemoBadge status={record.verification_status} />
      </div>

      {/* Record Title */}
      <h3 className="text-base font-bold text-slate-900 group-hover:text-blue-700 transition leading-snug line-clamp-2">
        <Link to={`/schemes/${record.id}`}>
          {displayName}
        </Link>
      </h3>

      {/* Department */}
      {record.department && (
        <p className="text-xs text-slate-500 mt-1 flex items-center gap-1.5 line-clamp-1">
          <Building2 className="w-3.5 h-3.5 text-slate-400 shrink-0" />
          {record.department}
        </p>
      )}

      {/* Description */}
      <p className="text-xs text-slate-600 mt-2.5 line-clamp-3 leading-relaxed flex-1">
        {displayDesc}
      </p>

      {/* Benefits pill */}
      {record.benefits && (
        <div className="mt-3.5 p-2.5 bg-slate-50 border border-slate-100 rounded-xl text-xs text-slate-700">
          <span className="font-semibold text-slate-900 block mb-0.5">Benefit:</span>
          <p className="line-clamp-2 text-slate-600 leading-snug">{record.benefits}</p>
        </div>
      )}

      {/* Action footer */}
      <div className="mt-4 pt-3.5 border-t border-slate-100 flex items-center justify-between gap-2">
        <Link
          to={`/checklist/${record.id}`}
          className="text-xs font-medium text-slate-600 hover:text-blue-700 flex items-center gap-1 py-1"
          title="Document checklist"
        >
          <CheckSquare className="w-3.5 h-3.5" />
          <span>Documents</span>
        </Link>

        <Link
          to={`/schemes/${record.id}`}
          className="inline-flex items-center gap-1 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg shadow-sm transition"
        >
          <span>View Details</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>
    </div>
  );
};
