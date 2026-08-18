import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.models.chat import ChatRole


class ChatMessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=4000)
    session_id: uuid.UUID | None = None  # omit to start a new session


class ChatMessageOut(BaseModel):
    id: uuid.UUID
    session_id: uuid.UUID
    role: ChatRole
    content: str
    cited_event_ids: list[str] | None
    cited_document_ids: list[str] | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatResponse(BaseModel):
    session_id: uuid.UUID
    message: ChatMessageOut


class ChatSessionOut(BaseModel):
    id: uuid.UUID
    title: str | None
    created_at: datetime
    messages: list[ChatMessageOut] = []

    model_config = {"from_attributes": True}
