"""
Eligibility router: check eligibility deterministically for single or all records.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.database import Record
from backend.app.models.schemas import CheckAllEligibilityRequest, EligibilityRequest, EligibilityResult
from backend.app.services.eligibility import evaluate_eligibility

router = APIRouter(prefix="/api/eligibility", tags=["eligibility"])


@router.post("/check", response_model=EligibilityResult)
def check_record_eligibility(data: EligibilityRequest, db: Session = Depends(get_db)):
    """Evaluate eligibility for a single record against the given citizen profile."""
    record = db.query(Record).filter(Record.id == data.record_id, Record.is_active.is_(True)).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    return evaluate_eligibility(data.record_id, data.profile, db)


@router.post("/check-all", response_model=list[EligibilityResult])
def check_all_records_eligibility(data: CheckAllEligibilityRequest, db: Session = Depends(get_db)):
    """Evaluate eligibility for all published schemes against the given profile."""
    records = db.query(Record).filter(
        Record.is_active.is_(True),
        Record.record_type == "scheme",
        Record.verification_status.in_(["verified", "demo"]),
    ).all()

    results = []
    for r in records:
        result = evaluate_eligibility(r.id, data.profile, db)
        results.append(result)

    # Sort results: eligible first, then insufficient_info, then not_eligible
    status_order = {"eligible": 0, "insufficient_info": 1, "not_eligible": 2}
    results.sort(key=lambda x: status_order.get(x.overall_status, 3))
    return results
