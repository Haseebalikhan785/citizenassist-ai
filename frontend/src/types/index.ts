export interface User {
  id: string;
  email: string;
  full_name: string;
  role: 'citizen' | 'admin';
  language_preference: string;
  profile_data: Record<string, any>;
  created_at?: string;
  is_active: boolean;
}

export interface EligibilityRule {
  id: string;
  record_id: string;
  field: string;
  operator: string;
  value: any;
  kind: string;
  source_url?: string;
  source_excerpt?: string;
  is_approved: boolean;
  description?: string;
}

export interface SchemeRecord {
  id: string;
  name: string;
  name_hi?: string;
  name_pa?: string;
  record_type: 'scheme' | 'service';
  description?: string;
  description_hi?: string;
  description_pa?: string;
  department?: string;
  level?: string;
  state_applicability?: string[];
  category?: string;
  target_beneficiaries?: string[];
  age_criteria?: { min?: number; max?: number };
  income_criteria?: { max_annual?: number };
  education_criteria?: string;
  other_conditions?: string[];
  benefits?: string;
  benefits_hi?: string;
  benefits_pa?: string;
  required_documents?: Array<{ name: string; description?: string; linked_service_id?: string | null } | string>;
  application_procedure?: string;
  application_url?: string;
  official_source_url?: string;
  source_excerpt?: string;
  last_verified_date?: string;
  verification_status: 'verified' | 'draft' | 'demo';
  source_document?: string;
  is_active: boolean;
  eligibility_rules?: EligibilityRule[];
}

export interface RuleResult {
  rule_id?: string;
  field: string;
  operator: string;
  value: any;
  status: 'MET' | 'NOT_MET' | 'UNKNOWN';
  kind?: string;
  source_url?: string;
  source_excerpt?: string;
  description: string;
  user_value?: any;
}

export interface EligibilityResult {
  record_id: string;
  record_name: string;
  overall_status: 'eligible' | 'not_eligible' | 'insufficient_info' | 'error';
  message: string;
  rule_results?: RuleResult[];
  category?: string;
  verification_status?: string;
}

export interface ChecklistItem {
  document_name: string;
  is_available: boolean;
  updated_at?: string;
  linked_service_id?: string | null;
}

export interface SearchResultItem {
  record_id: string;
  record_name: string;
  record_type: string;
  category: string;
  description?: string;
  score: number;
  matched_section: string;
  snippet: string;
  verification_status: string;
}

export interface ChatClaim {
  text: string;
  label?: 'verified' | 'inferred' | 'missing';
  source_ids?: string[];
  source_url?: string;
  source_title?: string;
  verified: boolean;
}

export interface AssistantStepInfo {
  understood?: Record<string, any>;
  retrieved?: string[];
  assessed?: Array<{ record_id: string; record_name: string; status: string; message: string }>;
  method?: string;
}

export interface ChatResponse {
  reply: string;
  session_id: string;
  claims: ChatClaim[];
  suggested_records: string[];
  profile_extracted?: Record<string, any>;
  steps?: AssistantStepInfo;
}

export interface SavedItem {
  id: string;
  record_id: string;
  record?: SchemeRecord;
  created_at?: string;
}
