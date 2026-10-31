import React from 'react';
import { SearchX } from 'lucide-react';

export const EmptyState: React.FC<{
  title?: string;
  description?: string;
  actionText?: string;
  onAction?: () => void;
}> = ({
  title = 'No results found',
  description = 'Try adjusting your filters, criteria, or search keywords.',
  actionText,
  onAction,
}) => {
  return (
    <div className="py-12 px-4 text-center bg-white rounded-2xl border border-slate-200 my-4 shadow-sm">
      <div className="w-12 h-12 bg-slate-100 text-slate-500 rounded-full flex items-center justify-center mx-auto mb-3">
        <SearchX className="w-6 h-6" />
      </div>
      <h3 className="text-base font-semibold text-slate-800">{title}</h3>
      <p className="text-sm text-slate-500 max-w-md mx-auto mt-1">{description}</p>
      {actionText && onAction && (
        <button
          onClick={onAction}
          className="mt-4 px-4 py-2 bg-blue-700 text-white text-xs font-semibold rounded-lg hover:bg-blue-800 transition"
        >
          {actionText}
        </button>
      )}
    </div>
  );
};
