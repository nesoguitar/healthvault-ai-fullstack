import enum
import uuid
from datetime import date, datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import BigInteger, Date, DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config import settings
from app.core.database import Base
from app.models.mixins import SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin


class DocumentType(str, enum.Enum):
    lab_report = "lab_report"
    imaging = "imaging"
    clinical_note = "clinical_note"
    discharge_summary = "discharge_summary"
    prescription = "prescription"
    other = "other"


class DocumentFileType(str, enum.Enum):
    pdf = "pdf"
    jpg = "jpg"
    png = "png"


class DocumentStatus(str, enum.Enum):
    processing = "processing"
    processed = "processed"
    failed = "failed"


class Document(UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, Base):
    """
    Uploaded medical record. The binary file itself never lives in Postgres —
    only `storage_key` (a path/blob-name) does. `extracted_text` and
    `embedding` are populated asynchronously by the document-processing
    pipeline (Azure Document Intelligence -> chunk -> embed).
    """
    __tablename__ = "documents"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True
    )

    file_name: Mapped[str] = mapped_column(String(500), nullable=False)
    document_type: Mapped[DocumentType] = mapped_column(
        Enum(DocumentType, name="document_type_enum"), default=DocumentType.other, nullable=False
    )
    file_type: Mapped[DocumentFileType] = mapped_column(
        Enum(DocumentFileType, name="document_file_type_enum"), nullable=False
    )
    size_kb: Mapped[int] = mapped_column(BigInteger, nullable=False)

    # Storage abstraction: local disk path in dev, Azure Blob key in prod.
    # See app/services/storage.py. Never store this as a public URL.
    storage_backend: Mapped[str] = mapped_column(String(20), nullable=False, default="local")
    storage_key: Mapped[str] = mapped_column(String(1000), nullable=False)
    content_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)  # SHA-256, dedup/integrity

    status: Mapped[DocumentStatus] = mapped_column(
        Enum(DocumentStatus, name="document_status_enum"),
        default=DocumentStatus.processing,
        nullable=False,
        index=True,
    )
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    extracted_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    processing_error: Mapped[str | None] = mapped_column(Text, nullable=True)

    # pgvector column for semantic search / RAG grounding in the AI chat.
    # Requires: CREATE EXTENSION IF NOT EXISTS vector; (see Alembic migration 0001).
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(settings.EMBEDDING_DIMENSIONS), nullable=True
    )

    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    patient: Mapped["Patient"] = relationship(back_populates="documents")

    def __repr__(self) -> str:
        return f"<Document {self.id} {self.file_name} status={self.status}>"
