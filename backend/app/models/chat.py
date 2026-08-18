import enum
import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config import settings
from app.core.database import Base
from app.models.mixins import UUIDPrimaryKeyMixin


class ChatRole(str, enum.Enum):
    user = "user"
    assistant = "assistant"


class ChatSession(UUIDPrimaryKeyMixin, Base):
    """Groups messages into a conversation thread."""
    __tablename__ = "chat_sessions"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    messages: Mapped[list["ChatMessage"]] = relationship(
        back_populates="session", cascade="all, delete-orphan", order_by="ChatMessage.created_at"
    )


class ChatMessage(UUIDPrimaryKeyMixin, Base):
    """
    A single turn in the AI assistant conversation. `cited_event_ids` and
    `cited_document_ids` record what grounded the assistant's answer (RAG
    provenance), which matters for a clinical-adjacent assistant: every
    claim should be traceable back to a record in the patient's own chart.
    """
    __tablename__ = "chat_messages"

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True
    )

    role: Mapped[ChatRole] = mapped_column(Enum(ChatRole, name="chat_role_enum"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    cited_event_ids: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    cited_document_ids: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)

    # Embedding of this message's content, enabling semantic recall of past
    # conversation turns as additional RAG context in later sessions.
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(settings.EMBEDDING_DIMENSIONS), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    session: Mapped["ChatSession"] = relationship(back_populates="messages")
    patient: Mapped["Patient"] = relationship(back_populates="chat_messages")

    def __repr__(self) -> str:
        return f"<ChatMessage {self.id} {self.role}>"
