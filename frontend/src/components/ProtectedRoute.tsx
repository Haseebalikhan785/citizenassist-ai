import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { LoadingSpinner } from './LoadingSpinner';

export const ProtectedRoute: React.FC<{ children: React.ReactNode; requireAdmin?: boolean }> = ({
  children,
  requireAdmin = false,
}) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <LoadingSpinner message="Checking authentication..." />;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (requireAdmin && user.role !== 'admin') {
    return (
      <div className="max-w-md mx-auto my-16 p-6 bg-white rounded-2xl border border-red-200 text-center shadow-sm">
        <h2 className="text-lg font-bold text-red-600">Access Denied (403)</h2>
        <p className="text-sm text-slate-600 mt-2">
          Administrator privileges are required to view this panel.
        </p>
      </div>
    );
  }

  return <>{children}</>;
};
