import React, { useEffect, useState } from 'react';
import {
  Shield,
  Upload,
  Globe,
  CheckCircle,
  XCircle,
  RefreshCw,
  FileText,
  AlertTriangle,
  ArrowRight,
  Database,
} from 'lucide-react';
import { api } from '../utils/api';
import { SchemeRecord } from '../types';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorMessage } from '../components/ErrorMessage';

export const Admin: React.FC = () => {
  const [drafts, setDrafts] = useState<SchemeRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Form states
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [urlInput, setUrlInput] = useState('');
  const [uploadingPdf, setUploadingPdf] = useState(false);
  const [importingUrl, setImportingUrl] = useState(false);

  const fetchDrafts = async () => {
    setLoading(true);
    try {
      const res = await api.admin.getIngestionLog();
      setDrafts(res);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch ingestion log');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDrafts();
  }, []);

  const handlePdfUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!pdfFile) return;

    setUploadingPdf(true);
    setMessage(null);
    setError(null);

    try {
      const res = await api.admin.uploadPdf(pdfFile);
      setMessage(res.message || 'PDF uploaded and draft generated successfully!');
      setPdfFile(null);
      fetchDrafts();
    } catch (err: any) {
      setError(err.message || 'PDF extraction failed');
    } finally {
      setUploadingPdf(false);
    }
  };

  const handleUrlImport = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!urlInput.trim()) return;

    setImportingUrl(true);
    setMessage(null);
    setError(null);

    try {
      const res = await api.admin.importUrl(urlInput.trim());
      setMessage(res.message || 'URL content imported and draft generated!');
      setUrlInput('');
      fetchDrafts();
    } catch (err: any) {
      setError(err.message || 'URL import failed');
    } finally {
      setImportingUrl(false);
    }
  };

  const handleApprove = async (recordId: string) => {
    setActionLoading(true);
    setMessage(null);
    setError(null);
    try {
      await api.admin.approve(recordId);
      setMessage('Draft scheme approved and published as verified! FTS5 index rebuilt.');
      fetchDrafts();
    } catch (err: any) {
      setError(err.message || 'Approval failed');
    } finally {
      setActionLoading(false);
    }
  };

  const handleReject = async (recordId: string) => {
    if (!window.confirm('Reject and delete this draft record?')) return;
    setActionLoading(true);
    setMessage(null);
    setError(null);
    try {
      await api.admin.reject(recordId);
      setMessage('Draft scheme rejected and removed.');
      fetchDrafts();
    } catch (err: any) {
      setError(err.message || 'Rejection failed');
    } finally {
      setActionLoading(false);
    }
  };

  const handleReindex = async () => {
    setActionLoading(true);
    setMessage(null);
    try {
      const res = await api.admin.reindex();
      setMessage(res.message);
    } catch (err: any) {
      setError(err.message || 'Reindexing failed');
    } finally {
      setActionLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Title */}
      <div className="flex items-center justify-between flex-wrap gap-4 pb-4 border-b border-slate-200">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <Shield className="w-6 h-6 text-amber-600" />
            Admin & Information Extraction Pipeline
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Supervised document ingestion: extract structured drafts from PDFs or official URLs, review citations, and publish.
          </p>
        </div>

        <button
          onClick={handleReindex}
          disabled={actionLoading}
          className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold rounded-xl shadow-sm transition flex items-center gap-1.5 disabled:opacity-50"
        >
          <Database className="w-4 h-4 text-blue-400" />
          <span>Rebuild Search Index</span>
        </button>
      </div>

      {message && (
        <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-2xl text-xs text-emerald-800 font-semibold flex items-center gap-2">
          <CheckCircle className="w-4 h-4 text-emerald-600 shrink-0" />
          <span>{message}</span>
        </div>
      )}

      {error && <ErrorMessage message={error} />}

      {/* Ingestion Pipeline Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* PDF Ingestion Card */}
        <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-2 text-blue-700">
              <Upload className="w-5 h-5" />
              <h2 className="text-sm font-bold text-slate-900">Upload Official Government PDF</h2>
            </div>
            <p className="text-xs text-slate-500 mb-4 leading-relaxed">
              Upload official gazettes, guidelines, or scheme circulars. Max 10MB, strictly validated PDF header. PyMuPDF extracts text, and AI generates a structured draft.
            </p>

            <form onSubmit={handlePdfUpload} className="space-y-3">
              <input
                type="file"
                accept=".pdf,application/pdf"
                onChange={(e) => setPdfFile(e.target.files?.[0] || null)}
                className="w-full text-xs text-slate-500 file:mr-3 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                required
              />

              <button
                type="submit"
                disabled={uploadingPdf || !pdfFile}
                className="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-xl transition shadow-sm disabled:opacity-50"
              >
                {uploadingPdf ? 'Extracting text and drafting...' : 'Extract & Generate Draft'}
              </button>
            </form>
          </div>

          <p className="text-[11px] text-slate-400 mt-4 italic">
            Demo sample available at: <code className="text-blue-600">data/documents/official_sc_scholarship_guidelines.pdf</code>
          </p>
        </div>

        {/* URL Import Card */}
        <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-2 text-indigo-700">
              <Globe className="w-5 h-5" />
              <h2 className="text-sm font-bold text-slate-900">Import from Verified URL</h2>
            </div>
            <p className="text-xs text-slate-500 mb-4 leading-relaxed">
              Extract public scheme information from official portal pages (.gov.in / .nic.in). Protected by strict SSRF filtering (HTTPS only, non-private IPs).
            </p>

            <form onSubmit={handleUrlImport} className="space-y-3">
              <input
                type="url"
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
                placeholder="https://scholarships.gov.in/..."
                className="w-full p-2.5 bg-slate-50 border border-slate-300 rounded-xl text-xs text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />

              <button
                type="submit"
                disabled={importingUrl || !urlInput.trim()}
                className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold rounded-xl transition shadow-sm disabled:opacity-50"
              >
                {importingUrl ? 'Fetching and parsing...' : 'Import & Generate Draft'}
              </button>
            </form>
          </div>

          <p className="text-[11px] text-slate-400 mt-4 italic">
            Respects robots.txt and blocks private network access.
          </p>
        </div>
      </div>

      {/* Review Section */}
      <section>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <FileText className="w-5 h-5 text-slate-700" />
            Extracted Drafts Pending Review ({drafts.length})
          </h2>
          <button
            onClick={fetchDrafts}
            className="text-xs text-blue-600 hover:underline flex items-center gap-1"
          >
            <RefreshCw className="w-3.5 h-3.5" /> Refresh
          </button>
        </div>

        {loading ? (
          <LoadingSpinner message="Checking ingestion queue..." />
        ) : drafts.length === 0 ? (
          <div className="p-8 bg-white rounded-3xl border border-slate-200 text-center shadow-sm">
            <CheckCircle className="w-10 h-10 text-emerald-500 mx-auto mb-2" />
            <h3 className="text-sm font-bold text-slate-800">Queue is Clear</h3>
            <p className="text-xs text-slate-500 mt-1">
              No draft records are waiting for approval. Upload a PDF or import a URL above to test the extraction workflow.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {drafts.map((draft) => (
              <div
                key={draft.id}
                className="p-5 bg-white rounded-3xl border border-amber-200 shadow-sm space-y-4"
              >
                <div className="flex items-start justify-between gap-4 flex-wrap pb-3 border-b border-slate-100">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-900">
                        STATUS: DRAFT
                      </span>
                      <span className="text-xs text-slate-500">{draft.category}</span>
                    </div>
                    <h3 className="text-base font-bold text-slate-900">{draft.name}</h3>
                    <p className="text-xs text-slate-500">{draft.department}</p>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleApprove(draft.id)}
                      disabled={actionLoading}
                      className="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-xl shadow-sm transition flex items-center gap-1.5"
                    >
                      <CheckCircle className="w-3.5 h-3.5" />
                      <span>Approve & Publish</span>
                    </button>

                    <button
                      onClick={() => handleReject(draft.id)}
                      disabled={actionLoading}
                      className="px-4 py-1.5 bg-red-600 hover:bg-red-700 text-white text-xs font-semibold rounded-xl shadow-sm transition flex items-center gap-1.5"
                    >
                      <XCircle className="w-3.5 h-3.5" />
                      <span>Reject</span>
                    </button>
                  </div>
                </div>

                {/* Side-by-side: Extracted Data vs Source Excerpt */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                  <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200">
                    <span className="font-bold text-slate-800 block mb-1">Extracted Details:</span>
                    <p className="text-slate-700 mb-2">{draft.description}</p>
                    <p className="text-slate-700">
                      <strong>Benefits:</strong> {draft.benefits}
                    </p>
                    <p className="text-slate-700 mt-1">
                      <strong>Target:</strong> {draft.target_beneficiaries?.join(', ')}
                    </p>
                  </div>

                  <div className="p-4 bg-amber-50/50 rounded-2xl border border-amber-200">
                    <span className="font-bold text-amber-900 block mb-1">Audited Source Excerpt:</span>
                    <blockquote className="italic text-slate-700">
                      "{draft.source_excerpt || 'No specific excerpt captured.'}"
                    </blockquote>
                    {draft.official_source_url && (
                      <span className="text-[11px] text-blue-700 underline block mt-2 break-all">
                        Source: {draft.official_source_url}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
};
