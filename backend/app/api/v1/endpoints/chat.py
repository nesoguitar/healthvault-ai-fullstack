"""
AI Chat API.

Every assistant reply is grounded in the patient's own structured records
(see app/services/chat_context.py) rather than the model's general
knowledge, and the safety framing in app/services/ai.py's SYSTEM_PROMPT
steers the model away from diagnosis/treatment advice and toward citing
what's actually in the record.
"""
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_patient
from app.models.chat import ChatMessage, ChatRole, ChatSession
from app.models.patient import Patient
from app.schemas.chat import ChatMessageCreate, ChatMessageOut, ChatResponse, ChatSessionOut
from app.services.ai import SYSTEM_PROMPT, get_ai_provider
from app.services.chat_context import build_patient_context

router = APIRouter()


@router.get("/sessions", response_model=list[ChatSessionOut])
def list_sessions(patient: Patient = Depends(get_current_patient), db: Session = Depends(get_db)):
    return (
        db.query(ChatSession)
        .filter(ChatSession.patient_id == patient.id)
        .order_by(ChatSession.created_at.desc())
        .all()
    )


@router.get("/sessions/{session_id}", response_model=ChatSessionOut)
def get_session(
    session_id: uuid.UUID,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id, ChatSession.patient_id == patient.id)
        .first()
    )
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found")
    return session


@router.post("/messages", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
def send_message(
    payload: ChatMessageCreate,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    if payload.session_id:
        session = (
            db.query(ChatSession)
            .filter(ChatSession.id == payload.session_id, ChatSession.patient_id == patient.id)
            .first()
        )
        if session is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found")
    else:
        session = ChatSession(patient_id=patient.id, title=payload.content[:80])
        db.add(session)
        db.flush()

    user_message = ChatMessage(
        session_id=session.id,
        patient_id=patient.id,
        role=ChatRole.user,
        content=payload.content,
    )
    db.add(user_message)

    ai = get_ai_provider()
    context = build_patient_context(db, patient)
    reply_text = ai.chat_completion(
        system_prompt=SYSTEM_PROMPT, context=context, user_message=payload.content
    )

    assistant_message = ChatMessage(
        session_id=session.id,
        patient_id=patient.id,
        role=ChatRole.assistant,
        content=reply_text,
    )
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)

    return ChatResponse(session_id=session.id, message=assistant_message)


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: uuid.UUID,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id, ChatSession.patient_id == patient.id)
        .first()
    )
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found")
    db.delete(session)
    db.commit()
