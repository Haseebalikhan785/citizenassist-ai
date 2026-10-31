"""
Saved items router: bookmark schemes to review later.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.security import get_current_user
from backend.app.models.database import Record, SavedItem, User
from backend.app.models.schemas import RecordResponse, SavedItemResponse

router = APIRouter(prefix="/api/saved", tags=["saved"])


@router.get("", response_model=list[SavedItemResponse])
def get_saved_items(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all saved items for the logged in user."""
    items = (
        db.query(SavedItem)
        .filter(SavedItem.user_id == current_user.id)
        .order_by(SavedItem.created_at.desc())
        .all()
    )

    results = []
    for item in items:
        rec = db.query(Record).filter(Record.id == item.record_id, Record.is_active.is_(True)).first()
        rec_resp = RecordResponse.model_validate(rec) if rec else None
        results.append(
            SavedItemResponse(
                id=item.id,
                record_id=item.record_id,
                record=rec_resp,
                created_at=item.created_at,
            )
        )
    return results


@router.post("/{record_id}")
def save_item(
    record_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Save/bookmark a record."""
    record = db.query(Record).filter(Record.id == record_id, Record.is_active.is_(True)).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    existing = (
        db.query(SavedItem)
        .filter(SavedItem.user_id == current_user.id, SavedItem.record_id == record_id)
        .first()
    )
    if not existing:
        saved = SavedItem(user_id=current_user.id, record_id=record_id)
        db.add(saved)
        db.commit()

    return {"message": "Record saved successfully"}


@router.delete("/{record_id}")
def remove_saved_item(
    record_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Remove a bookmarked record."""
    item = (
        db.query(SavedItem)
        .filter(SavedItem.user_id == current_user.id, SavedItem.record_id == record_id)
        .first()
    )
    if item:
        db.delete(item)
        db.commit()

    return {"message": "Record removed from saved items"}
