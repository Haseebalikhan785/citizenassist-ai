"""
Pydantic v2 schemas for request/response validation.
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, EmailStr, Field


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

class UserCreate(BaseModel):
    email: str = Field(..., min_length=5)
    password: str = Field(..., min_length=6)
    full_name: str = ""
    language_preference: str = "en"


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    language_preference: str
    profile_data: dict[str, Any] = {}
    created_at: datetime | None = None
    is_active: bool = True

    model_config = {"from_attributes": True}


class UserProfile(BaseModel):
    full_name: str | None = None
    language_preference: str | None = None
    profile_data: dict[str, Any] | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ---------------------------------------------------------------------------
# Records
# ---------------------------------------------------------------------------

class EligibilityRuleCreate(BaseModel):
    field: str
    operator: str
    value: Any
    kind: str = "profile"
    source_url: str | None = None
    source_excerpt: str | None = None
    is_approved: bool = False
    description: str | None = None


class EligibilityRuleResponse(BaseModel):
    id: str
    record_id: str
    field: str
    operator: str
    value: Any
    kind: str
    source_url: str | None = None
    source_excerpt: str | None = None
    is_approved: bool
    description: str | None = None

    model_config = {"from_attributes": True}


class RecordCreate(BaseModel):
    name: str
    name_hi: str | None = None
    name_pa: str | None = None
    record_type: str  # "scheme" or "service"
    description: str | None = None
    description_hi: str | None = None
    description_pa: str | None = None
    department: str | None = None
    level: str | None = None
    state_applicability: list[str] | None = None
    category: str | None = None
    target_beneficiaries: list[str] | None = None
    age_criteria: dict | None = None
    income_criteria: dict | None = None
    education_criteria: str | None = None
    other_conditions: list[str] | None = None
    benefits: str | None = None
    benefits_hi: str | None = None
    benefits_pa: str | None = None
    required_documents: list[dict] | None = None
    application_procedure: str | None = None
    application_url: str | None = None
    official_source_url: str | None = None
    source_excerpt: str | None = None
    verification_status: str = "draft"
    eligibility_rules: list[EligibilityRuleCreate] | None = None


class RecordUpdate(BaseModel):
    name: str | None = None
    name_hi: str | None = None
    name_pa: str | None = None
    record_type: str | None = None
    description: str | None = None
    description_hi: str | None = None
    description_pa: str | None = None
    department: str | None = None
    level: str | None = None
    state_applicability: list[str] | None = None
    category: str | None = None
    target_beneficiaries: list[str] | None = None
    age_criteria: dict | None = None
    income_criteria: dict | None = None
    education_criteria: str | None = None
    other_conditions: list[str] | None = None
    benefits: str | None = None
    benefits_hi: str | None = None
    benefits_pa: str | None = None
    required_documents: list[dict] | None = None
    application_procedure: str | None = None
    application_url: str | None = None
    official_source_url: str | None = None
    source_excerpt: str | None = None
    verification_status: str | None = None
    is_active: bool | None = None


class RecordResponse(BaseModel):
    id: str
    name: str
    name_hi: str | None = None
    name_pa: str | None = None
    record_type: str
    description: str | None = None
    description_hi: str | None = None
    description_pa: str | None = None
    department: str | None = None
    level: str | None = None
    state_applicability: list[str] | None = None
    category: str | None = None
    target_beneficiaries: list[str] | None = None
    age_criteria: dict | None = None
    income_criteria: dict | None = None
    education_criteria: str | None = None
    other_conditions: list[str] | None = None
    benefits: str | None = None
    benefits_hi: str | None = None
    benefits_pa: str | None = None
    required_documents: list[dict] | None = None
    application_procedure: str | None = None
    application_url: str | None = None
    official_source_url: str | None = None
    source_excerpt: str | None = None
    last_verified_date: str | None = None
    fetched_at: datetime | None = None
    verification_status: str = "demo"
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None
    eligibility_rules: list[EligibilityRuleResponse] = []

    model_config = {"from_attributes": True}


class RecordListResponse(BaseModel):
    records: list[RecordResponse]
    total: int
    page: int = 1
    per_page: int = 20


class RecordDetailResponse(RecordResponse):
    pass


class CheckAllEligibilityRequest(BaseModel):
    profile: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Eligibility
# ---------------------------------------------------------------------------

class EligibilityRequest(BaseModel):
    record_id: str | None = None
    profile: dict[str, Any] = {}


class RuleResult(BaseModel):
    rule_id: str | None = None
    field: str
    operator: str
    value: Any
    status: str  # MET, NOT_MET, UNKNOWN
    description: str | None = None
    user_value: Any | None = None


class EligibilityResult(BaseModel):
    record_id: str
    record_name: str
    overall_status: str  # eligible, not_eligible, insufficient_info
    message: str
    rule_results: list[RuleResult] = []
    category: str | None = None
    verification_status: str = "demo"


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    category: str | None = None
    state: str | None = None
    record_type: str | None = None
    limit: int = 10
    top_k: int = 10


class SearchResultItem(BaseModel):
    record_id: str
    record_name: str
    record_type: str
    category: str | None = None
    description: str | None = None
    score: float = 0.0
    matched_section: str | None = None
    snippet: str | None = None
    verification_status: str = "demo"


class SearchResponse(BaseModel):
    results: list[SearchResultItem]
    total: int
    query: str
    search_method: str = "keyword"
    method: str = "keyword"  # keyword, embedding, hybrid


# ---------------------------------------------------------------------------
# Chat / Assistant
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    session_id: str | None = None
    language: str = "en"
    profile: dict[str, Any] | None = None


class ChatClaim(BaseModel):
    text: str
    source_url: str | None = None
    verified: bool = False


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    claims: list[ChatClaim] = []
    suggested_records: list[str] = []  # record IDs
    profile_extracted: dict[str, Any] | None = None


# ---------------------------------------------------------------------------
# Checklist
# ---------------------------------------------------------------------------

class ChecklistUpdate(BaseModel):
    document_name: str
    is_available: bool


class ChecklistItemResponse(BaseModel):
    document_name: str
    is_available: bool
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class ChecklistResponse(BaseModel):
    record_id: str
    items: list[ChecklistItemResponse]


# ---------------------------------------------------------------------------
# Saved Items
# ---------------------------------------------------------------------------

class SavedItemResponse(BaseModel):
    id: str
    record_id: str
    record: RecordResponse | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Feedback
# ---------------------------------------------------------------------------

class FeedbackCreate(BaseModel):
    record_id: str | None = None
    feedback_type: str  # incorrect_info, missing_info, broken_link, other
    description: str


class FeedbackResponse(BaseModel):
    id: str
    user_id: str | None = None
    record_id: str | None = None
    feedback_type: str
    description: str
    status: str
    created_at: datetime | None = None

    model_config = {"from_attributes": True}
