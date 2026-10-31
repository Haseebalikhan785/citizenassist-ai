"""
Records router: list, detail, categories, CRUD (admin-protected).
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.security import get_current_admin
from backend.app.models.database import Record, EligibilityRule
from backend.app.models.schemas import (
    RecordCreate,
    RecordDetailResponse,
    RecordListResponse,
    RecordResponse,
    RecordUpdate,
)

router = APIRouter(prefix="/api/records", tags=["records"])


@router.get("", response_model=RecordListResponse)
def list_records(
    category: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    record_type: Optional[str] = Query(None),
    beneficiary: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List published/verified/demo records with multi-facet filtering."""
    query = db.query(Record).filter(
        Record.is_active.is_(True),
        Record.verification_status.in_(["verified", "demo"]),
    )

    if category:
        query = query.filter(Record.category == category)

    if record_type:
        query = query.filter(Record.record_type == record_type)

    if q:
        search_pattern = f"%{q.strip()}%"
        query = query.filter(
            or_(
                Record.name.ilike(search_pattern),
                Record.description.ilike(search_pattern),
                Record.department.ilike(search_pattern),
            )
        )

    all_records = query.all()

    # In-memory filtering for JSON list fields (state and beneficiary)
    filtered = []
    for r in all_records:
        if state:
            states = r.state_applicability or []
            s_lowers = [s.lower() for s in states]
            if "all india" not in s_lowers and state.lower() not in s_lowers:
                continue
        if beneficiary:
            b_list = r.target_beneficiaries or []
            b_lowers = [b.lower() for b in b_list]
            if not any(beneficiary.lower() in b for b in b_lowers):
                continue
        filtered.append(r)

    total = len(filtered)
    paged = filtered[skip : skip + limit]

    return RecordListResponse(
        total=total,
        records=[RecordResponse.model_validate(r) for r in paged],
    )


@router.get("/categories", response_model=list[str])
def list_categories(db: Session = Depends(get_db)):
    """List distinct categories from existing records."""
    cats = (
        db.query(Record.category)
        .filter(Record.is_active.is_(True), Record.category.isnot(None))
        .distinct()
        .all()
    )
    result = [c[0] for c in cats if c[0]]
    if not result:
        result = [
            "Education and Scholarships",
            "Agriculture and Farmers",
            "Healthcare",
            "Employment",
            "Financial Assistance",
            "Women and Child Welfare",
            "Housing",
            "Social Security",
            "Other Citizen Services",
        ]
    return sorted(result)


@router.get("/{record_id}", response_model=RecordDetailResponse)
def get_record(record_id: str, db: Session = Depends(get_db)):
    """Get a single record along with its approved eligibility rules."""
    record = db.query(Record).filter(Record.id == record_id, Record.is_active.is_(True)).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    rules = (
        db.query(EligibilityRule)
        .filter(EligibilityRule.record_id == record_id)
        .all()
    )

    rec_data = RecordResponse.model_validate(record).model_dump()
    rec_data["eligibility_rules"] = [r for r in rules]
    return RecordDetailResponse(**rec_data)


@router.post("", response_model=RecordResponse)
def create_record(
    data: RecordCreate,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin: create a new record."""
    record = Record(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return RecordResponse.model_validate(record)


@router.put("/{record_id}", response_model=RecordResponse)
def update_record(
    record_id: str,
    data: RecordUpdate,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin: update an existing record."""
    record = db.query(Record).filter(Record.id == record_id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    for field, val in data.model_dump(exclude_unset=True).items():
        setattr(record, field, val)

    db.commit()
    db.refresh(record)
    return RecordResponse.model_validate(record)


@router.delete("/{record_id}")
def delete_record(
    record_id: str,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin: soft-delete a record."""
    record = db.query(Record).filter(Record.id == record_id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    record.is_active = False
    db.commit()
    return {"message": "Record deactivated successfully"}
