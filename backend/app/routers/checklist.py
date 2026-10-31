"""
Checklist router: fetch required documents for a scheme and persist progress for logged in users.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.security import get_current_user, get_current_user_optional
from backend.app.models.database import ChecklistProgress, Record
from backend.app.models.schemas import ChecklistItemResponse, ChecklistResponse, ChecklistUpdate

router = APIRouter(prefix="/api/checklist", tags=["checklist"])


@router.get("/{record_id}", response_model=ChecklistResponse)
def get_checklist(
    record_id: str,
    current_user=Depends(get_current_user_optional),
    db: Session = Depends(get_db),
):
    """Get the document checklist for a scheme, populated with user's saved progress if logged in."""
    record = db.query(Record).filter(Record.id == record_id, Record.is_active.is_(True)).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    docs = record.required_documents or []
    # If docs is a list of dicts: [{"name": "Aadhaar Card", "description": "..."}]
    # or list of strings
    normalized_docs = []
    for d in docs:
        if isinstance(d, dict):
            name = d.get("name", "")
            linked_service_id = d.get("linked_service_id")
        else:
            name = str(d)
            linked_service_id = None
        if name:
            normalized_docs.append({"name": name, "linked_service_id": linked_service_id})

    # Fetch user's saved availability
    user_avail = {}
    if current_user:
        prog = (
            db.query(ChecklistProgress)
            .filter(
                ChecklistProgress.user_id == current_user.id,
                ChecklistProgress.record_id == record_id,
            )
            .all()
        )
        for p in prog:
            user_avail[p.document_name] = p.is_available

    items = []
    for doc in normalized_docs:
        name = doc["name"]
        items.append(
            ChecklistItemResponse(
                document_name=name,
                is_available=user_avail.get(name, False),
                updated_at=None,
            )
        )

    return ChecklistResponse(record_id=record_id, items=items)


@router.put("/{record_id}")
def update_checklist(
    record_id: str,
    data: ChecklistUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update availability of a specific document in the checklist."""
    prog = (
        db.query(ChecklistProgress)
        .filter(
            ChecklistProgress.user_id == current_user.id,
            ChecklistProgress.record_id == record_id,
            ChecklistProgress.document_name == data.document_name,
        )
        .first()
    )

    if prog:
        prog.is_available = data.is_available
    else:
        prog = ChecklistProgress(
            user_id=current_user.id,
            record_id=record_id,
            document_name=data.document_name,
            is_available=data.is_available,
        )
        db.add(prog)

    db.commit()
    return {"message": "Checklist updated successfully"}
