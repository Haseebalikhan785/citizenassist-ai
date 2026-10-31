import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { User, ShieldAlert, Trash2, CheckCircle2 } from 'lucide-react';
import { api } from '../utils/api';
import { useAuth } from '../hooks/useAuth';
import { useTranslation, Language } from '../i18n';

export const Profile: React.FC = () => {
  const { user, refreshUser, logout } = useAuth();
  const { language, setLanguage, t } = useTranslation();
  const navigate = useNavigate();

  const [fullName, setFullName] = useState(user?.full_name || '');
  const [langPref, setLangPref] = useState(user?.language_preference || language);

  // Profile data criteria
  const p = user?.profile_data || {};
  const [age, setAge] = useState<string>(p.age ? String(p.age) : '20');
  const [state, setState] = useState<string>(p.state || 'Punjab');
  const [incomeLakh, setIncomeLakh] = useState<string>(
    p.annual_family_income ? String(p.annual_family_income / 100000) : '2.0'
  );
  const [occupation, setOccupation] = useState<string>(p.occupation || 'student');
  const [category, setCategory] = useState<string>(p.category || 'SC');
  const [gender, setGender] = useState<string>(p.gender || 'male');

  const [saving, setSaving] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState(false);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setSavedSuccess(false);

    const numericAge = parseInt(age, 10);
    const numericIncome = Math.round(parseFloat(incomeLakh || '0') * 100000);

    try {
      await api.profile.update({
        full_name: fullName.trim(),
        language_preference: langPref,
        profile_data: {
          age: isNaN(numericAge) ? undefined : numericAge,
          state,
          annual_family_income: isNaN(numericIncome) ? undefined : numericIncome,
          occupation,
          category,
          gender,
        },
      });
      setLanguage(langPref as Language);
      await refreshUser();
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3000);
    } catch (err) {
      console.error('Failed to update profile', err);
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteAccount = async () => {
    if (!window.confirm('Are you absolutely sure? This will permanently delete your account, saved schemes, checklist progress, and chat history.')) {
      return;
    }
    try {
      await api.auth.deleteAccount();
      await logout();
      navigate('/');
    } catch (e) {
      console.error('Delete account failed', e);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
          <User className="w-6 h-6 text-blue-600" />
          Citizen Profile & Settings
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Manage your saved profile attributes used for automatic eligibility assessments and recommendations.
        </p>
      </div>

      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 sm:p-8 space-y-6">
        {savedSuccess && (
          <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-xs text-emerald-800 font-semibold flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            Profile updated successfully!
          </div>
        )}

        <form onSubmit={handleSave} className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="text-xs font-semibold text-slate-700 block mb-1">Full Name</label>
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                className="w-full text-xs p-2.5 bg-slate-50 border border-slate-300 rounded-xl"
                placeholder="e.g. Rajesh Kumar"
              />
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-700 block mb-1">Email Address</label>
              <input
                type="email"
                disabled
                value={user?.email || ''}
                className="w-full text-xs p-2.5 bg-slate-100 border border-slate-200 rounded-xl text-slate-500 cursor-not-allowed"
              />
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-700 block mb-1">Preferred Language</label>
              <select
                value={langPref}
                onChange={(e) => setLangPref(e.target.value)}
                className="w-full text-xs p-2.5 bg-slate-50 border border-slate-300 rounded-xl"
              >
                <option value="en">English</option>
                <option value="hi">हिंदी (Hindi)</option>
                <option value="pa">ਪੰਜਾਬੀ (Punjabi)</option>
              </select>
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-700 block mb-1">Age</label>
              <input
                type="number"
                min="0"
                max="120"
                value={age}
                onChange={(e) => setAge(e.target.value)}
                className="w-full text-xs p-2.5 bg-slate-50 border border-slate-300 rounded-xl"
              />
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-700 block mb-1">State</label>
              <select
                value={state}
                onChange={(e) => setState(e.target.value)}
                className="w-full text-xs p-2.5 bg-slate-50 border border-slate-300 rounded-xl"
              >
                <option value="Punjab">Punjab</option>
                <option value="Haryana">Haryana</option>
                <option value="Delhi">Delhi</option>
                <option value="Uttar Pradesh">Uttar Pradesh</option>
                <option value="Rajasthan">Rajasthan</option>
                <option value="Other">Other State</option>
              </select>
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-700 block mb-1">Annual Family Income (in Lakhs)</label>
              <input
                type="number"
                step="0.1"
                value={incomeLakh}
                onChange={(e) => setIncomeLakh(e.target.value)}
                className="w-full text-xs p-2.5 bg-slate-50 border border-slate-300 rounded-xl"
                placeholder="2.0"
              />
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-700 block mb-1">Occupation</label>
              <select
                value={occupation}
                onChange={(e) => setOccupation(e.target.value)}
                className="w-full text-xs p-2.5 bg-slate-50 border border-slate-300 rounded-xl"
              >
                <option value="student">Student</option>
                <option value="farmer">Farmer</option>
                <option value="artisan">Artisan / Craftsperson</option>
                <option value="unorganized_worker">Unorganized Worker</option>
                <option value="self_employed">Self Employed</option>
                <option value="unemployed">Unemployed</option>
              </select>
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-700 block mb-1">Social Category</label>
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

            <div>
              <label className="text-xs font-semibold text-slate-700 block mb-1">Gender</label>
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
          </div>

          <div className="pt-4 border-t border-slate-100 flex justify-end">
            <button
              type="submit"
              disabled={saving}
              className="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-xl shadow-sm transition disabled:opacity-50"
            >
              {saving ? 'Saving changes...' : 'Save Profile'}
            </button>
          </div>
        </form>

        {/* Privacy Note */}
        <div className="p-4 bg-slate-50 border border-slate-200 rounded-2xl text-[11px] text-slate-600 leading-relaxed">
          <strong className="text-slate-800">Privacy & Consent Note:</strong> We collect minimal personal data solely to evaluate eligibility criteria deterministically. All fields are optional. Your personal data is stored locally in your private database and is never sold or shared.
        </div>

        {/* Delete Account */}
        <div className="pt-6 border-t border-slate-200 flex items-center justify-between gap-4 flex-wrap">
          <div>
            <h3 className="text-xs font-bold text-red-600">Delete Account & Stored Data</h3>
            <p className="text-[11px] text-slate-500 mt-0.5">
              Permanently delete your user credentials, saved schemes, checklist progress, and chat history.
            </p>
          </div>

          <button
            type="button"
            onClick={handleDeleteAccount}
            className="px-4 py-2 border border-red-300 text-red-600 hover:bg-red-50 text-xs font-semibold rounded-xl transition flex items-center gap-1.5"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span>Delete my account and data</span>
          </button>
        </div>
      </div>
    </div>
  );
};
