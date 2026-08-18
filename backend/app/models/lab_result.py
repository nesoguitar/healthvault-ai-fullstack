import enum
import uuid
from datetime import date

from sqlalchemy import Date, Enum, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class LabFlag(str, enum.Enum):
    normal = "normal"
    high = "high"
    low = "low"
    critical = "critical"


class LabResult(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """
    A single lab observation. History/trend charts are built by querying
    all rows for the same (patient_id, test_name) ordered by result_date —
    there is no separate "history" blob, so every point is independently
    auditable back to its source document.
    """
    __tablename__ = "lab_results"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True
    )

    test_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(50), nullable=False)
    reference_range: Mapped[str] = mapped_column(String(100), nullable=False)
    flag: Mapped[LabFlag] = mapped_column(Enum(LabFlag, name="lab_flag_enum"), nullable=False, index=True)

    result_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    ordered_by: Mapped[str] = mapped_column(String(255), nullable=False)

    source_document_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"), nullable=True
    )

    patient: Mapped["Patient"] = relationship(back_populates="lab_results")
    source_document: Mapped["Document | None"] = relationship()

    def __repr__(self) -> str:
        return f"<LabResult {self.id} {self.test_name}={self.value}{self.unit}>"
