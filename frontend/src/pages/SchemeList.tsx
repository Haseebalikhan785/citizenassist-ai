import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Search, Filter, RefreshCw, X } from 'lucide-react';
import { api } from '../utils/api';
import { SchemeRecord } from '../types';
import { RecordCard } from '../components/RecordCard';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorMessage } from '../components/ErrorMessage';
import { EmptyState } from '../components/EmptyState';
import { useTranslation } from '../i18n';

export const SchemeList: React.FC = () => {
  const { t } = useTranslation();
  const [searchParams, setSearchParams] = useSearchParams();

  const [records, setRecords] = useState<SchemeRecord[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filters from URL
  const selectedCategory = searchParams.get('category') || '';
  const selectedType = searchParams.get('type') || '';
  const selectedState = searchParams.get('state') || '';
  const selectedBeneficiary = searchParams.get('beneficiary') || '';
  const searchQuery = searchParams.get('q') || '';

  const [searchInput, setSearchInput] = useState(searchQuery);

  const fetchRecords = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.records.list({
        category: selectedCategory || undefined,
        record_type: selectedType || undefined,
        state: selectedState || undefined,
        beneficiary: selectedBeneficiary || undefined,
        q: searchQuery || undefined,
      });
      setRecords(res.records);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch schemes');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const fetchCats = async () => {
      try {
        const cats = await api.records.categories();
        setCategories(cats);
      } catch (e) {
        console.error('Failed to load categories', e);
      }
    };
    fetchCats();
  }, []);

  useEffect(() => {
    fetchRecords();
  }, [selectedCategory, selectedType, selectedState, selectedBeneficiary, searchQuery]);

  const updateParam = (key: string, val: string) => {
    const next = new URLSearchParams(searchParams);
    if (val) {
      next.set(key, val);
    } else {
      next.delete(key);
    }
    setSearchParams(next);
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    updateParam('q', searchInput.trim());
  };

  const clearAllFilters = () => {
    setSearchInput('');
    setSearchParams(new URLSearchParams());
  };

  const hasActiveFilters = Boolean(
    selectedCategory || selectedType || selectedState || selectedBeneficiary || searchQuery
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
          Government Schemes & Citizen Services
        </h1>
        <p className="text-xs sm:text-sm text-slate-600 mt-1">
          Explore genuine welfare programs, verify statutory eligibility conditions, and find official application links.
        </p>
      </div>

      {/* Search Bar */}
      <form onSubmit={handleSearchSubmit} className="mb-6">
        <div className="relative flex items-center">
          <Search className="w-5 h-5 text-slate-400 absolute left-4 pointer-events-none" />
          <input
            type="text"
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            placeholder="Search by keyword, scheme name, or department..."
            className="w-full pl-11 pr-24 py-3 bg-white border border-slate-300 rounded-xl text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm"
          />
          <button
            type="submit"
            className="absolute right-2 px-4 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg shadow-sm transition"
          >
            Search
          </button>
        </div>
      </form>

      {/* Layout: Sidebar Filter + Cards Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 items-start">
        {/* Filters Sidebar */}
        <aside className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-5 lg:sticky lg:top-20">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <span className="text-xs font-bold text-slate-900 flex items-center gap-1.5">
              <Filter className="w-4 h-4 text-slate-500" /> Filters
            </span>
            {hasActiveFilters && (
              <button
                onClick={clearAllFilters}
                className="text-[11px] text-blue-600 hover:underline flex items-center gap-0.5"
              >
                <X className="w-3 h-3" /> Clear all
              </button>
            )}
          </div>

          {/* Record Type filter */}
          <div>
            <label className="text-xs font-semibold text-slate-700 block mb-1.5">Type</label>
            <div className="grid grid-cols-3 gap-1 bg-slate-100 p-1 rounded-lg text-xs font-medium">
              <button
                type="button"
                onClick={() => updateParam('type', '')}
                className={`py-1 rounded text-center transition ${!selectedType ? 'bg-white shadow text-slate-900' : 'text-slate-600'}`}
              >
                All
              </button>
              <button
                type="button"
                onClick={() => updateParam('type', 'scheme')}
                className={`py-1 rounded text-center transition ${selectedType === 'scheme' ? 'bg-white shadow text-slate-900' : 'text-slate-600'}`}
              >
                Schemes
              </button>
              <button
                type="button"
                onClick={() => updateParam('type', 'service')}
                className={`py-1 rounded text-center transition ${selectedType === 'service' ? 'bg-white shadow text-slate-900' : 'text-slate-600'}`}
              >
                Services
              </button>
            </div>
          </div>

          {/* Category filter */}
          <div>
            <label className="text-xs font-semibold text-slate-700 block mb-1.5">Category</label>
            <select
              value={selectedCategory}
              onChange={(e) => updateParam('category', e.target.value)}
              className="w-full text-xs p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
              <option value="">All Categories</option>
              {categories.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>

          {/* State filter */}
          <div>
            <label className="text-xs font-semibold text-slate-700 block mb-1.5">State</label>
            <select
              value={selectedState}
              onChange={(e) => updateParam('state', e.target.value)}
              className="w-full text-xs p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
              <option value="">All India / Any State</option>
              <option value="Punjab">Punjab</option>
              <option value="Haryana">Haryana</option>
              <option value="Delhi">Delhi</option>
              <option value="Uttar Pradesh">Uttar Pradesh</option>
              <option value="Rajasthan">Rajasthan</option>
            </select>
          </div>

          {/* Beneficiary Type */}
          <div>
            <label className="text-xs font-semibold text-slate-700 block mb-1.5">Target Beneficiary</label>
            <select
              value={selectedBeneficiary}
              onChange={(e) => updateParam('beneficiary', e.target.value)}
              className="w-full text-xs p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
              <option value="">All Beneficiaries</option>
              <option value="student">Students</option>
              <option value="farmer">Farmers / Agriculture</option>
              <option value="women">Women</option>
              <option value="senior">Senior Citizens</option>
              <option value="artisan">Artisans / Craftsmen</option>
              <option value="worker">Unorganized Workers</option>
            </select>
          </div>
        </aside>

        {/* Records Results */}
        <section className="lg:col-span-3">
          {error && <ErrorMessage message={error} onRetry={fetchRecords} />}

          {loading ? (
            <LoadingSpinner message="Searching verified schemes & services..." />
          ) : records.length === 0 ? (
            <EmptyState
              title="No schemes or services match your criteria"
              description="Try changing the category or clearing specific filters."
              actionText="Reset All Filters"
              onAction={clearAllFilters}
            />
          ) : (
            <div>
              <div className="flex items-center justify-between mb-4 text-xs text-slate-500">
                <span>Showing <strong>{records.length}</strong> verified entries</span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {records.map((r) => (
                  <RecordCard key={r.id} record={r} />
                ))}
              </div>
            </div>
          )}
        </section>
      </div>
    </div>
  );
};
