import React from 'react';

export const DemoBadge: React.FC<{ status?: string }> = ({ status = 'demo' }) => {
  if (status === 'verified') {
    return (
      <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-300">
        ✓ VERIFIED DATA
      </span>
    );
  }
  return (
    <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold bg-amber-100 text-amber-900 border border-amber-300">
      DEMO DATA
    </span>
  );
};
