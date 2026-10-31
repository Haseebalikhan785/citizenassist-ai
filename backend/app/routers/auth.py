"""
Authentication router: register, login, logout, me, delete account.
Tokens are stored in httpOnly cookies for security.
"""

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.security import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from backend.app.models.database import User
from backend.app.models.schemas import TokenResponse, UserCreate, UserLogin, UserResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(data: UserCreate, response: Response, db: Session = Depends(get_db)):
    """Register a new citizen user."""
    existing = db.query(User).filter(User.email == data.email.lower().strip()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists",
        )

    user = User(
        email=data.email.lower().strip(),
        hashed_password=hash_password(data.password),
        full_name=data.full_name or "",
        role="citizen",
        language_preference=data.language_preference or "en",
        profile_data={},
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.id, "role": user.role, "email": user.email})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,  # Allow http on localhost
        max_age=86400,
    )
    return TokenResponse(access_token=token, token_type="bearer", user=UserResponse.model_validate(user))


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, response: Response, db: Session = Depends(get_db)):
    """Log in an existing user."""
    user = db.query(User).filter(User.email == data.email.lower().strip()).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )

    token = create_access_token({"sub": user.id, "role": user.role, "email": user.email})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=86400,
    )
    return TokenResponse(access_token=token, token_type="bearer", user=UserResponse.model_validate(user))


@router.post("/logout")
def logout(response: Response):
    """Log out user by clearing the auth cookie."""
    response.delete_cookie(key="access_token")
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    """Get the currently authenticated user."""
    return UserResponse.model_validate(current_user)


@router.delete("/account")
def delete_account(
    response: Response,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete current user's account and personal data."""
    # Remove user records
    from backend.app.models.database import ChecklistProgress, SavedItem, Feedback, ChatHistory
    db.query(ChecklistProgress).filter(ChecklistProgress.user_id == current_user.id).delete()
    db.query(SavedItem).filter(SavedItem.user_id == current_user.id).delete()
    db.query(Feedback).filter(Feedback.user_id == current_user.id).delete()
    db.query(ChatHistory).filter(ChatHistory.user_id == current_user.id).delete()
    db.delete(current_user)
    db.commit()

    response.delete_cookie(key="access_token")
    return {"message": "Account and all associated data deleted successfully"}
