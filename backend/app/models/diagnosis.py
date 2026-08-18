import enum
import uuid
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class DiagnosisStatus(str, enum.Enum):
    active = "active"
    resolved = "resolved"
    chronic = "chronic"
    in_remission = "in_remission"


class DiagnosisSeverity(str, enum.Enum):
    mild = "mild"
    moderate = "moderate"
    severe = "severe"


class Diagnosis(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "diagnoses"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True
    )

    condition: Mapped[str] = mapped_column(String(255), nullable=False)
    icd10_code: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    diagnosed_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[DiagnosisStatus] = mapped_column(
        Enum(DiagnosisStatus, name="diagnosis_status_enum"), nullable=False, index=True
    )
    severity: Mapped[DiagnosisSeverity] = mapped_column(
        Enum(DiagnosisSeverity, name="diagnosis_severity_enum"), nullable=False
    )
    diagnosed_by: Mapped[str] = mapped_column(String(255), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    patient: Mapped["Patient"] = relationship(back_populates="diagnoses")

    def __repr__(self) -> str:
        return f"<Diagnosis {self.id} {self.condition}>"
