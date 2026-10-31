"""
Feedback router: citizen issue reporting on incorrect info or broken links.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.security import get_current_admin, get_current_user_optional
from backend.app.models.database import Feedback
from backend.app.models.schemas import FeedbackCreate, FeedbackResponse

router = APIRouter(prefix="/api/feedback", tags=["feedback"])


@router.post("", response_model=FeedbackResponse)
def submit_feedback(
    data: FeedbackCreate,
    current_user=Depends(get_current_user_optional),
    db: Session = Depends(get_db),
):
    """Submit citizen feedback on scheme data, link issues, or missing information."""
    fb = Feedback(
        user_id=current_user.id if current_user else None,
        record_id=data.record_id,
        feedback_type=data.feedback_type,
        description=data.description,
        status="pending",
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return FeedbackResponse.model_validate(fb)


@router.get("", response_model=list[FeedbackResponse])
def list_feedback(
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin: view all citizen feedback."""
    items = db.query(Feedback).order_by(Feedback.created_at.desc()).all()
    return [FeedbackResponse.model_validate(f) for f in items]
