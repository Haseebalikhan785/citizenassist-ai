import {
  ChatResponse,
  ChecklistItem,
  EligibilityResult,
  SavedItem,
  SchemeRecord,
  SearchResultItem,
  User,
} from '../types';

const API_BASE = '/api';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(errorData.detail || `HTTP Error ${res.status}`);
  }

  return res.json();
}

export const api = {
  auth: {
    login: (data: { email: string; password: string }) =>
      request<{ access_token: string; user: User }>('/auth/login', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    register: (data: { email: string; password: string; full_name?: string; language_preference?: string }) =>
      request<{ access_token: string; user: User }>('/auth/register', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    me: () => request<User>('/auth/me'),
    logout: () => request<{ message: string }>('/auth/logout', { method: 'POST' }),
    deleteAccount: () => request<{ message: string }>('/auth/account', { method: 'DELETE' }),
  },
  records: {
    list: (params?: { category?: string; state?: string; record_type?: string; beneficiary?: string; q?: string }) => {
      const searchParams = new URLSearchParams();
      if (params) {
        Object.entries(params).forEach(([k, v]) => {
          if (v) searchParams.append(k, v);
        });
      }
      return request<{ total: number; records: SchemeRecord[] }>(`/records?${searchParams.toString()}`);
    },
    get: (id: string) => request<SchemeRecord>(`/records/${id}`),
    categories: () => request<string[]>('/records/categories'),
  },
  eligibility: {
    check: (recordId: string, profile: Record<string, any>) =>
      request<EligibilityResult>('/eligibility/check', {
        method: 'POST',
        body: JSON.stringify({ record_id: recordId, profile }),
      }),
    checkAll: (profile: Record<string, any>) =>
      request<EligibilityResult[]>('/eligibility/check-all', {
        method: 'POST',
        body: JSON.stringify({ profile }),
      }),
  },
  search: {
    query: (queryText: string, filters?: { category?: string; state?: string; record_type?: string }) =>
      request<{ query: string; results: SearchResultItem[]; total: number; search_method: string }>('/search', {
        method: 'POST',
        body: JSON.stringify({ query: queryText, ...filters }),
      }),
  },
  checklist: {
    get: (recordId: string) => request<{ record_id: string; items: ChecklistItem[] }>(`/checklist/${recordId}`),
    update: (recordId: string, documentName: string, isAvailable: boolean) =>
      request<{ message: string }>(`/checklist/${recordId}`, {
        method: 'PUT',
        body: JSON.stringify({ document_name: documentName, is_available: isAvailable }),
      }),
  },
  saved: {
    list: () => request<SavedItem[]>('/saved'),
    save: (recordId: string) => request<{ message: string }>(`/saved/${recordId}`, { method: 'POST' }),
    remove: (recordId: string) => request<{ message: string }>(`/saved/${recordId}`, { method: 'DELETE' }),
  },
  assistant: {
    chat: (data: { message: string; session_id?: string; language?: string; profile?: Record<string, any> }) =>
      request<ChatResponse>('/assistant/chat', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    extractProfile: (message: string) =>
      request<{ extracted: Record<string, any> }>('/assistant/extract-profile', {
        method: 'POST',
        body: JSON.stringify({ message }),
      }),
  },
  profile: {
    get: () => request<User>('/profile'),
    update: (data: { full_name?: string; language_preference?: string; profile_data?: Record<string, any> }) =>
      request<User>('/profile', {
        method: 'PUT',
        body: JSON.stringify(data),
      }),
  },
  feedback: {
    submit: (data: { record_id?: string; feedback_type: string; description: string }) =>
      request<{ id: string; status: string }>('/feedback', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
  },
  admin: {
    uploadPdf: async (file: File) => {
      const formData = new FormData();
      formData.append('file', file);
      const res = await fetch('/api/admin/upload-pdf', {
        method: 'POST',
        credentials: 'include',
        body: formData,
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: 'Upload failed' }));
        throw new Error(err.detail || 'Upload failed');
      }
      return res.json();
    },
    importUrl: (url: string) =>
      request<{ message: string; record_id: string }>('/admin/import-url', {
        method: 'POST',
        body: JSON.stringify({ url }),
      }),
    approve: (recordId: string) =>
      request<{ message: string }>(`/admin/records/${recordId}/approve`, {
        method: 'PUT',
      }),
    reject: (recordId: string) =>
      request<{ message: string }>(`/admin/records/${recordId}/reject`, {
        method: 'PUT',
      }),
    getIngestionLog: () => request<SchemeRecord[]>('/admin/ingestion-log'),
    reindex: () => request<{ message: string }>('/admin/reindex', { method: 'POST' }),
  },
};
