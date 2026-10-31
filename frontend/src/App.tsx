import React, { Suspense, lazy } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/Layout';
import { LoadingSpinner } from './components/LoadingSpinner';
import { ProtectedRoute } from './components/ProtectedRoute';
import { AuthProvider } from './hooks/useAuth';
import { LanguageProvider } from './i18n';

// Lazy-loaded routes for performance & low bandwidth
const Landing = lazy(() => import('./pages/Landing').then((m) => ({ default: m.Landing })));
const SchemeList = lazy(() => import('./pages/SchemeList').then((m) => ({ default: m.SchemeList })));
const SchemeDetail = lazy(() => import('./pages/SchemeDetail').then((m) => ({ default: m.SchemeDetail })));
const Eligibility = lazy(() => import('./pages/Eligibility').then((m) => ({ default: m.Eligibility })));
const Checklist = lazy(() => import('./pages/Checklist').then((m) => ({ default: m.Checklist })));
const Assistant = lazy(() => import('./pages/Assistant').then((m) => ({ default: m.Assistant })));
const Dashboard = lazy(() => import('./pages/Dashboard').then((m) => ({ default: m.Dashboard })));
const Comparison = lazy(() => import('./pages/Comparison').then((m) => ({ default: m.Comparison })));
const Profile = lazy(() => import('./pages/Profile').then((m) => ({ default: m.Profile })));
const Login = lazy(() => import('./pages/Login').then((m) => ({ default: m.Login })));
const Register = lazy(() => import('./pages/Register').then((m) => ({ default: m.Register })));
const Admin = lazy(() => import('./pages/Admin').then((m) => ({ default: m.Admin })));
const About = lazy(() => import('./pages/About').then((m) => ({ default: m.About })));

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <LanguageProvider>
        <AuthProvider>
          <Suspense fallback={<LoadingSpinner message="Loading CitizenAssist..." />}>
            <Routes>
              <Route path="/" element={<Layout />}>
                <Route index element={<Landing />} />
                <Route path="schemes" element={<SchemeList />} />
                <Route path="schemes/:id" element={<SchemeDetail />} />
                <Route path="eligibility" element={<Eligibility />} />
                <Route path="checklist/:recordId" element={<Checklist />} />
                <Route path="assistant" element={<Assistant />} />
                <Route path="compare" element={<Comparison />} />
                <Route
                  path="dashboard"
                  element={
                    <ProtectedRoute>
                      <Dashboard />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="profile"
                  element={
                    <ProtectedRoute>
                      <Profile />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="admin"
                  element={
                    <ProtectedRoute requireAdmin>
                      <Admin />
                    </ProtectedRoute>
                  }
                />
                <Route path="about" element={<About />} />
                <Route path="login" element={<Login />} />
                <Route path="register" element={<Register />} />
                <Route path="*" element={<Navigate to="/" replace />} />
              </Route>
            </Routes>
          </Suspense>
        </AuthProvider>
      </LanguageProvider>
    </BrowserRouter>
  );
};

export default App;
