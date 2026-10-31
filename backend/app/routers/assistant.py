"""
Assistant router: AI chat, profile extraction, and session chat history.
"""

from uuid import uuid4
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.security import get_current_user_optional
from backend.app.models.database import ChatHistory
from backend.app.models.schemas import ChatRequest, ChatResponse
from backend.app.services.assistant import execute_agentic_chat, extract_profile_from_text

router = APIRouter(prefix="/api/assistant", tags=["assistant"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    data: ChatRequest,
    current_user=Depends(get_current_user_optional),
    db: Session = Depends(get_db),
):
    """
    Main AI Assistant conversation endpoint.
    Runs the grounded agentic workflow (understand, retrieve, assess, compose, validate).
    """
    session_id = data.session_id or str(uuid4())

    # Load recent conversation history if session exists
    history = (
        db.query(ChatHistory)
        .filter(ChatHistory.session_id == session_id)
        .order_by(ChatHistory.created_at.asc())
        .limit(10)
        .all()
    )
    history_dicts = [{"role": h.role, "content": h.content} for h in history]

    # Save user message
    user_msg = ChatHistory(
        user_id=current_user.id if current_user else None,
        session_id=session_id,
        role="user",
        content=data.message,
    )
    db.add(user_msg)
    db.commit()

    # Determine user profile: merge request profile with logged-in user's stored profile
    combined_profile = {}
    if current_user and current_user.profile_data:
        combined_profile.update(current_user.profile_data)
    if data.profile:
        combined_profile.update(data.profile)

    response = await execute_agentic_chat(
        query=data.message,
        session_id=session_id,
        db=db,
        user_profile=combined_profile,
        language=data.language or "en",
        chat_history=history_dicts,
    )

    # Save assistant response
    asst_msg = ChatHistory(
        user_id=current_user.id if current_user else None,
        session_id=session_id,
        role="assistant",
        content=response.reply,
        metadata_={
            "claims": [c.model_dump() for c in response.claims],
            "suggested_records": response.suggested_records,
            "profile_extracted": response.profile_extracted,
            "steps": response.steps.model_dump() if response.steps else None,
        },
    )
    db.add(asst_msg)
    db.commit()

    return response


@router.post("/extract-profile")
def extract_profile(data: dict):
    """Extract profile fields from user natural language query."""
    message = data.get("message", "")
    extracted = extract_profile_from_text(message)
    return {"extracted": extracted}


@router.get("/history/{session_id}")
def get_chat_history(session_id: str, db: Session = Depends(get_db)):
    """Retrieve message history for a given chat session."""
    messages = (
        db.query(ChatHistory)
        .filter(ChatHistory.session_id == session_id)
        .order_by(ChatHistory.created_at.asc())
        .all()
    )
    return [
        {
            "id": m.id,
            "role": m.role,
            "content": m.content,
            "metadata": m.metadata_,
            "created_at": m.created_at,
        }
        for m in messages
    ]
