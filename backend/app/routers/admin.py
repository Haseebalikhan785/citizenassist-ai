"""
Admin router: document extraction (PDF/URL), draft approval/rejection, reindexing.
Protected by get_current_admin dependency.
"""

from typing import Any
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.security import get_current_admin
from backend.app.models.database import EligibilityRule, Record, SearchChunk
from backend.app.models.schemas import RecordResponse
from backend.app.services.extraction import (
    extract_text_from_pdf,
    extract_text_from_url,
    generate_draft_record_with_gemini,
)
from backend.app.services.search import build_fts_index

router = APIRouter(prefix="/api/admin", tags=["admin"])


class ImportUrlRequest(BaseModel):
    url: str


@router.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """
    Upload official government PDF (max 10MB, %PDF header validation),
    extract text, and generate a draft record with source excerpts.
    """
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files (.pdf) are allowed",
        )

    # Read content
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds maximum limit of 10 MB",
        )

    # Magic byte check: must start with %PDF
    if not content.startswith(b"%PDF"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format: Not a genuine PDF document",
        )

    try:
        raw_text = extract_text_from_pdf(content)
        if not raw_text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not extract readable text from PDF",
            )

        draft_data = generate_draft_record_with_gemini(raw_text, source_url=f"Uploaded PDF: {file.filename}")

        # Create draft record
        draft_rules = draft_data.pop("draft_rules", [])
        record = Record(
            name=draft_data.get("name", file.filename),
            record_type=draft_data.get("record_type", "scheme"),
            description=draft_data.get("description", ""),
            department=draft_data.get("department", ""),
            level=draft_data.get("level", "central"),
            state_applicability=draft_data.get("state_applicability", ["All India"]),
            category=draft_data.get("category", "Social Security"),
            target_beneficiaries=draft_data.get("target_beneficiaries", []),
            benefits=draft_data.get("benefits", ""),
            required_documents=draft_data.get("required_documents", []),
            application_procedure=draft_data.get("application_procedure", ""),
            official_source_url=draft_data.get("official_source_url", ""),
            source_excerpt=draft_data.get("source_excerpt", ""),
            source_document=file.filename,
            verification_status="draft",
        )
        db.add(record)
        db.flush()

        for r in draft_rules:
            rule = EligibilityRule(
                record_id=record.id,
                field=r.get("field", "age"),
                operator=r.get("operator", "=="),
                value=r.get("value", 0),
                kind=r.get("kind", "profile"),
                source_excerpt=r.get("source_excerpt", ""),
                description=r.get("description", ""),
                is_approved=False,
            )
            db.add(rule)

        db.commit()
        db.refresh(record)

        return {
            "message": "PDF uploaded and draft record generated successfully",
            "record_id": record.id,
            "draft_record": RecordResponse.model_validate(record),
            "rules_count": len(draft_rules),
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Extraction failed: {str(e)}",
        )


@router.post("/import-url")
async def import_url(
    data: ImportUrlRequest,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """
    Import and extract government scheme info from a public HTTPS URL.
    Includes SSRF protection.
    """
    try:
        raw_text = await extract_text_from_url(data.url)
        draft_data = generate_draft_record_with_gemini(raw_text, source_url=data.url)

        draft_rules = draft_data.pop("draft_rules", [])
        record = Record(
            name=draft_data.get("name", "Imported Scheme"),
            record_type=draft_data.get("record_type", "scheme"),
            description=draft_data.get("description", ""),
            department=draft_data.get("department", ""),
            level=draft_data.get("level", "central"),
            state_applicability=draft_data.get("state_applicability", ["All India"]),
            category=draft_data.get("category", "Social Security"),
            target_beneficiaries=draft_data.get("target_beneficiaries", []),
            benefits=draft_data.get("benefits", ""),
            required_documents=draft_data.get("required_documents", []),
            application_procedure=draft_data.get("application_procedure", ""),
            official_source_url=data.url,
            source_excerpt=draft_data.get("source_excerpt", ""),
            verification_status="draft",
        )
        db.add(record)
        db.flush()

        for r in draft_rules:
            rule = EligibilityRule(
                record_id=record.id,
                field=r.get("field", "age"),
                operator=r.get("operator", "=="),
                value=r.get("value", 0),
                kind=r.get("kind", "profile"),
                source_excerpt=r.get("source_excerpt", ""),
                description=r.get("description", ""),
                is_approved=False,
            )
            db.add(rule)

        db.commit()
        db.refresh(record)

        return {
            "message": "URL imported and draft record generated successfully",
            "record_id": record.id,
            "draft_record": RecordResponse.model_validate(record),
        }

    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Import failed: {str(e)}",
        )


@router.put("/records/{record_id}/approve")
def approve_record(
    record_id: str,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Approve a draft record, publish it as verified, and index it in FTS5."""
    record = db.query(Record).filter(Record.id == record_id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    record.verification_status = "verified"

    # Approve all associated rules
    rules = db.query(EligibilityRule).filter(EligibilityRule.record_id == record_id).all()
    for r in rules:
        r.is_approved = True

    # Generate search chunks for the approved record
    sections = [
        ("description", f"{record.name}. {record.description}"),
        ("benefits", f"Benefits of {record.name}: {record.benefits}"),
        ("procedure", f"Application procedure for {record.name}: {record.application_procedure}"),
    ]
    for sec_name, content in sections:
        if content.strip():
            chunk = SearchChunk(
                record_id=record.id,
                section=sec_name,
                content=content,
                source_url=record.official_source_url,
            )
            db.add(chunk)

    db.commit()

    # Rebuild FTS index
    build_fts_index(db)

    return {"message": "Record approved, published and reindexed successfully"}


@router.put("/records/{record_id}/reject")
def reject_record(
    record_id: str,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Reject a draft record."""
    record = db.query(Record).filter(Record.id == record_id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    db.query(EligibilityRule).filter(EligibilityRule.record_id == record_id).delete()
    db.query(SearchChunk).filter(SearchChunk.record_id == record_id).delete()
    db.delete(record)
    db.commit()

    return {"message": "Record rejected and removed"}


@router.get("/ingestion-log")
def get_ingestion_log(
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Get all draft records pending review."""
    drafts = (
        db.query(Record)
        .filter(Record.verification_status == "draft")
        .order_by(Record.created_at.desc())
        .all()
    )
    return [RecordResponse.model_validate(d) for d in drafts]


@router.post("/reindex")
def trigger_reindex(
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Manually trigger FTS index rebuilding."""
    count = build_fts_index(db)
    return {"message": f"Search index successfully rebuilt with {count} chunks"}
