import React from 'react';
import { CheckCircle2, XCircle, HelpCircle } from 'lucide-react';

export const EligibilityBadge: React.FC<{ status: 'eligible' | 'not_eligible' | 'insufficient_info' | 'error' | string }> = ({
  status,
}) => {
  if (status === 'eligible') {
    return (
      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
        <CheckCircle2 className="w-3.5 h-3.5" />
        Potentially Eligible
      </span>
    );
  }

  if (status === 'not_eligible') {
    return (
      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-red-50 text-red-700 border border-red-200">
        <XCircle className="w-3.5 h-3.5" />
        Not Eligible
      </span>
    );
  }

  return (
    <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-50 text-amber-700 border border-amber-200">
      <HelpCircle className="w-3.5 h-3.5" />
      Information Needed
    </span>
  );
};
