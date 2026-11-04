import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Menu, X, Globe, User as UserIcon, Shield, Sparkles } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { useTranslation, Language } from '../i18n';

export const Header: React.FC = () => {
  const { user, logout, guestLogin } = useAuth();
  const { language, setLanguage, t } = useTranslation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  const handleGuestTour = async () => {
    try {
      await guestLogin();
      navigate('/dashboard');
    } catch (e) {
      navigate('/login');
    }
  };

  return (
    <header className="sticky top-0 z-40 bg-slate-900 text-white shadow-md border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-3 group focus:outline-none focus:ring-2 focus:ring-blue-400 rounded-lg p-1">
            <div className="w-9 h-9 rounded-xl bg-blue-600 flex items-center justify-center font-bold text-white shadow-sm group-hover:bg-blue-500 transition">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <span className="text-lg font-bold tracking-tight text-white block leading-tight">
                CitizenAssist <span className="text-blue-400">AI</span>
              </span>
              <span className="text-[10px] text-slate-400 block font-normal tracking-wide">
                Intelligent Public Service Navigator
              </span>
            </div>
          </Link>

          {/* Desktop Navigation Links */}
          <nav className="hidden md:flex items-center gap-1 lg:gap-2">
            <Link
              to="/schemes"
              className="px-3 py-1.5 text-xs lg:text-sm font-medium text-slate-300 hover:text-white hover:bg-slate-800 rounded-lg transition"
            >
              {t('nav.schemes')}
            </Link>
            <Link
              to="/assistant"
              className="px-3 py-1.5 text-xs lg:text-sm font-medium text-blue-300 hover:text-white hover:bg-slate-800 rounded-lg transition flex items-center gap-1.5"
            >
              <Sparkles className="w-3.5 h-3.5" />
              {t('nav.assistant')}
            </Link>
            <Link
              to="/eligibility"
              className="px-3 py-1.5 text-xs lg:text-sm font-medium text-slate-300 hover:text-white hover:bg-slate-800 rounded-lg transition"
            >
              {t('nav.eligibility')}
            </Link>
            <Link
              to="/compare"
              className="px-3 py-1.5 text-xs lg:text-sm font-medium text-slate-300 hover:text-white hover:bg-slate-800 rounded-lg transition"
            >
              {t('nav.compare')}
            </Link>
            {user && (
              <Link
                to="/dashboard"
                className="px-3 py-1.5 text-xs lg:text-sm font-medium text-slate-300 hover:text-white hover:bg-slate-800 rounded-lg transition"
              >
                {t('nav.dashboard')}
              </Link>
            )}
            {user?.role === 'admin' && (
              <Link
                to="/admin"
                className="px-3 py-1.5 text-xs lg:text-sm font-medium text-amber-400 hover:text-amber-300 hover:bg-slate-800 rounded-lg transition flex items-center gap-1"
              >
                <Shield className="w-3.5 h-3.5" />
                {t('nav.admin')}
              </Link>
            )}
            <Link
              to="/about"
              className="px-3 py-1.5 text-xs lg:text-sm font-medium text-slate-300 hover:text-white hover:bg-slate-800 rounded-lg transition"
            >
              {t('nav.about')}
            </Link>
          </nav>

          {/* Right Actions: Language Selector + Auth */}
          <div className="hidden md:flex items-center gap-3">
            {/* Language Switcher */}
            <div className="flex items-center bg-slate-800 rounded-lg p-0.5 border border-slate-700">
              {(['en', 'hi', 'pa'] as Language[]).map((lang) => (
                <button
                  key={lang}
                  onClick={() => setLanguage(lang)}
                  className={`px-2.5 py-1 text-xs font-semibold rounded-md transition ${
                    language === lang
                      ? 'bg-blue-600 text-white shadow-sm'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                  aria-label={`Switch language to ${lang}`}
                >
                  {lang === 'en' ? 'EN' : lang === 'hi' ? 'हिं' : 'ਪੰ'}
                </button>
              ))}
            </div>

            {/* User Profile / Auth */}
            {user ? (
              <div className="flex items-center gap-2">
                <Link
                  to="/profile"
                  className="flex items-center gap-1.5 text-xs font-medium text-slate-300 hover:text-white px-2.5 py-1.5 rounded-lg hover:bg-slate-800 transition"
                >
                  <UserIcon className="w-4 h-4 text-blue-400" />
                  <span className="max-w-[100px] truncate">{user.full_name || user.email.split('@')[0]}</span>
                </Link>
                <button
                  onClick={handleLogout}
                  className="px-3 py-1.5 text-xs font-medium text-red-300 hover:text-red-200 hover:bg-slate-800 rounded-lg transition"
                >
                  {t('nav.logout')}
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link
                  to="/login"
                  className="px-3 py-1.5 text-xs font-semibold text-slate-200 hover:text-white hover:bg-slate-800 rounded-lg transition"
                >
                  {t('nav.login')}
                </Link>
                <Link
                  to="/register"
                  className="px-3.5 py-1.5 text-xs font-semibold bg-blue-600 hover:bg-blue-500 text-white rounded-lg shadow-sm transition"
                >
                  {t('nav.register')}
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="flex md:hidden items-center gap-2">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 text-slate-300 hover:text-white hover:bg-slate-800 rounded-lg transition"
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-slate-900 border-b border-slate-800 px-4 pt-2 pb-4 space-y-2">
          {/* Mobile Language Switcher */}
          <div className="flex items-center justify-between py-2 border-b border-slate-800">
            <span className="text-xs text-slate-400 flex items-center gap-1.5">
              <Globe className="w-4 h-4" /> Language / ਭਾਸ਼ਾ / भाषा
            </span>
            <div className="flex items-center bg-slate-800 rounded-lg p-0.5 border border-slate-700">
              {(['en', 'hi', 'pa'] as Language[]).map((lang) => (
                <button
                  key={lang}
                  onClick={() => setLanguage(lang)}
                  className={`px-2.5 py-1 text-xs font-semibold rounded-md transition ${
                    language === lang ? 'bg-blue-600 text-white' : 'text-slate-400'
                  }`}
                >
                  {lang === 'en' ? 'EN' : lang === 'hi' ? 'हिं' : 'ਪੰ'}
                </button>
              ))}
            </div>
          </div>

          <Link
            to="/schemes"
            onClick={() => setMobileMenuOpen(false)}
            className="block px-3 py-2 text-sm font-medium text-slate-300 hover:bg-slate-800 rounded-lg"
          >
            {t('nav.schemes')}
          </Link>
          <Link
            to="/assistant"
            onClick={() => setMobileMenuOpen(false)}
            className="block px-3 py-2 text-sm font-medium text-blue-400 hover:bg-slate-800 rounded-lg"
          >
            {t('nav.assistant')}
          </Link>
          <Link
            to="/eligibility"
            onClick={() => setMobileMenuOpen(false)}
            className="block px-3 py-2 text-sm font-medium text-slate-300 hover:bg-slate-800 rounded-lg"
          >
            {t('nav.eligibility')}
          </Link>
          <Link
            to="/compare"
            onClick={() => setMobileMenuOpen(false)}
            className="block px-3 py-2 text-sm font-medium text-slate-300 hover:bg-slate-800 rounded-lg"
          >
            {t('nav.compare')}
          </Link>
          {user && (
            <Link
              to="/dashboard"
              onClick={() => setMobileMenuOpen(false)}
              className="block px-3 py-2 text-sm font-medium text-slate-300 hover:bg-slate-800 rounded-lg"
            >
              {t('nav.dashboard')}
            </Link>
          )}
          {user?.role === 'admin' && (
            <Link
              to="/admin"
              onClick={() => setMobileMenuOpen(false)}
              className="block px-3 py-2 text-sm font-medium text-amber-400 hover:bg-slate-800 rounded-lg"
            >
              {t('nav.admin')}
            </Link>
          )}
          <Link
            to="/about"
            onClick={() => setMobileMenuOpen(false)}
            className="block px-3 py-2 text-sm font-medium text-slate-300 hover:bg-slate-800 rounded-lg"
          >
            {t('nav.about')}
          </Link>

          <div className="pt-2 border-t border-slate-800">
            {user ? (
              <div className="space-y-2">
                <Link
                  to="/profile"
                  onClick={() => setMobileMenuOpen(false)}
                  className="block px-3 py-2 text-sm font-medium text-slate-300 hover:bg-slate-800 rounded-lg"
                >
                  {t('nav.profile')} ({user.email})
                </Link>
                <button
                  onClick={() => {
                    handleLogout();
                    setMobileMenuOpen(false);
                  }}
                  className="w-full text-left px-3 py-2 text-sm font-medium text-red-400 hover:bg-slate-800 rounded-lg"
                >
                  {t('nav.logout')}
                </button>
              </div>
            ) : (
              <div className="flex gap-2 pt-1">
                <Link
                  to="/login"
                  onClick={() => setMobileMenuOpen(false)}
                  className="flex-1 text-center py-2 text-sm font-medium bg-slate-800 text-slate-200 rounded-lg"
                >
                  {t('nav.login')}
                </Link>
                <Link
                  to="/register"
                  onClick={() => setMobileMenuOpen(false)}
                  className="flex-1 text-center py-2 text-sm font-medium bg-blue-600 text-white rounded-lg"
                >
                  {t('nav.register')}
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </header>
  );
};
