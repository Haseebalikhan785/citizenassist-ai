"""
SQLAlchemy ORM models for CitizenAssist AI.
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    JSON,
    String,
    Text,
)

from backend.app.core.database import Base


def _uuid() -> str:
    return str(uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=_uuid)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, default="")
    role = Column(String, default="citizen")  # citizen or admin
    language_preference = Column(String, default="en")
    profile_data = Column(JSON, default=dict)  # age, state, income, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class Record(Base):
    __tablename__ = "records"

    id = Column(String, primary_key=True, default=_uuid)
    name = Column(String, nullable=False)
    name_hi = Column(String, nullable=True)
    name_pa = Column(String, nullable=True)
    record_type = Column(String, nullable=False)  # "scheme" or "service"
    description = Column(Text)
    description_hi = Column(Text, nullable=True)
    description_pa = Column(Text, nullable=True)
    department = Column(String)
    level = Column(String)  # "central" or "state"
    state_applicability = Column(JSON)  # list of states or ["All India"]
    category = Column(String)  # Education, Agriculture, Healthcare, etc.
    target_beneficiaries = Column(JSON)  # list of strings
    age_criteria = Column(JSON)  # {"min": int, "max": int} or null
    income_criteria = Column(JSON)  # {"max_annual": int} or null
    education_criteria = Column(String, nullable=True)
    other_conditions = Column(JSON)  # list of condition strings
    benefits = Column(Text)
    benefits_hi = Column(Text, nullable=True)
    benefits_pa = Column(Text, nullable=True)
    required_documents = Column(JSON)  # list of {"name", "description", "linked_service_id"?}
    application_procedure = Column(Text)
    application_url = Column(String, nullable=True)
    official_source_url = Column(String, nullable=True)
    source_excerpt = Column(Text, nullable=True)
    last_verified_date = Column(String, nullable=True)
    fetched_at = Column(DateTime, nullable=True)
    verification_status = Column(String, default="demo")  # verified, draft, demo
    source_document = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_records_category", "category"),
        Index("idx_records_type", "record_type"),
        Index("idx_records_status", "verification_status"),
    )


class EligibilityRule(Base):
    __tablename__ = "eligibility_rules"

    id = Column(String, primary_key=True, default=_uuid)
    record_id = Column(String, ForeignKey("records.id"), nullable=False, index=True)
    field = Column(String, nullable=False)  # age, state, annual_family_income, etc.
    operator = Column(String, nullable=False)  # <=, >=, ==, in, not_in, between
    value = Column(JSON, nullable=False)  # the comparison value
    kind = Column(String, default="profile")  # profile or document
    source_url = Column(String, nullable=True)
    source_excerpt = Column(String, nullable=True)
    is_approved = Column(Boolean, default=False)
    description = Column(String, nullable=True)  # human-readable description


class SearchChunk(Base):
    __tablename__ = "search_chunks"

    id = Column(String, primary_key=True, default=_uuid)
    record_id = Column(String, ForeignKey("records.id"), nullable=False, index=True)
    section = Column(String, nullable=False)  # eligibility, benefits, documents, procedure, description
    content = Column(Text, nullable=False)
    source_url = Column(String, nullable=True)
    embedding = Column(JSON, nullable=True)  # stored as list of floats


class SavedItem(Base):
    __tablename__ = "saved_items"

    id = Column(String, primary_key=True, default=_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    record_id = Column(String, ForeignKey("records.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ChecklistProgress(Base):
    __tablename__ = "checklist_progress"

    id = Column(String, primary_key=True, default=_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    record_id = Column(String, ForeignKey("records.id"), nullable=False)
    document_name = Column(String, nullable=False)
    is_available = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.utcnow)


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(String, primary_key=True, default=_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)  # null for guests
    session_id = Column(String, nullable=False, index=True)
    role = Column(String, nullable=False)  # user or assistant
    content = Column(Text, nullable=False)
    metadata_ = Column("metadata", JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(String, primary_key=True, default=_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    record_id = Column(String, ForeignKey("records.id"), nullable=True)
    feedback_type = Column(String)  # incorrect_info, missing_info, broken_link, other
    description = Column(Text)
    status = Column(String, default="pending")  # pending, reviewed, resolved
    created_at = Column(DateTime, default=datetime.utcnow)
