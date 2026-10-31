"""
User profile router: get and update citizen profile details.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.security import get_current_user
from backend.app.models.database import User
from backend.app.models.schemas import UserProfile, UserResponse

router = APIRouter(prefix="/api/profile", tags=["profile"])


@router.get("", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    """Get the profile of current user."""
    return UserResponse.model_validate(current_user)


@router.put("", response_model=UserResponse)
def update_profile(
    data: UserProfile,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update profile fields (full name, language preference, profile criteria data)."""
    if data.full_name is not None:
        current_user.full_name = data.full_name
    if data.language_preference is not None:
        current_user.language_preference = data.language_preference
    if data.profile_data is not None:
        # Merge or update profile fields
        existing = dict(current_user.profile_data or {})
        existing.update(data.profile_data)
        current_user.profile_data = existing

    db.commit()
    db.refresh(current_user)
    return UserResponse.model_validate(current_user)
