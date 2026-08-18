"""
Access/audit log — required under HIPAA's audit controls standard
(45 CFR § 164.312(b)) for systems that create, modify, or access ePHI.

This is an append-only table: rows are never updated or deleted by the
application (no ORM relationship exposes update/delete for it). In
production, additionally ship these rows to a write-once log sink
(e.g. Azure Monitor / Log Analytics) so they survive a compromise of the
primary database.
"""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import UUIDPrimaryKeyMixin


class AuditLog(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "audit_logs"

    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)

    actor_user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    actor_ip: Mapped[str | None] = mapped_column(String(64), nullable=True)

    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # e.g. "patient.read"
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g. "Document"
    resource_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)

    status_code: Mapped[int] = mapped_column(nullable=False)
    detail: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    def __repr__(self) -> str:
        return f"<AuditLog {self.action} {self.resource_type}:{self.resource_id} by {self.actor_user_id}>"
