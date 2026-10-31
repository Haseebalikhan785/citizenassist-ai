import React from 'react';
import { AlertCircle } from 'lucide-react';

export const ErrorMessage: React.FC<{ message: string; onRetry?: () => void }> = ({
  message,
  onRetry,
}) => {
  return (
    <div className="p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 flex items-start gap-3 my-4">
      <AlertCircle className="w-5 h-5 shrink-0 mt-0.5 text-red-600" />
      <div className="flex-1 text-sm">
        <p className="font-semibold text-red-800">Something went wrong</p>
        <p className="mt-1">{message}</p>
        {onRetry && (
          <button
            onClick={onRetry}
            className="mt-2 px-3 py-1 bg-red-600 text-white text-xs font-medium rounded-lg hover:bg-red-700 transition"
          >
            Try Again
          </button>
        )}
      </div>
    </div>
  );
};
