import enum
import uuid
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.mixins import SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin


class MedicalEventType(str, enum.Enum):
    office_visit = "office_visit"
    hospitalization = "hospitalization"
    procedure = "procedure"
    lab_result = "lab_result"
    imaging_study = "imaging_study"
    medication_started = "medication_started"


class MedicalEvent(UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, Base):
    """A single entry on the patient's chronological health timeline."""
    __tablename__ = "medical_events"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True
    )

    event_type: Mapped[MedicalEventType] = mapped_column(
        Enum(MedicalEventType, name="medical_event_type_enum"), nullable=False, index=True
    )
    event_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    provider: Mapped[str | None] = mapped_column(String(255), nullable=True)
    facility: Mapped[str | None] = mapped_column(String(255), nullable=True)
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)

    related_document_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"), nullable=True
    )

    patient: Mapped["Patient"] = relationship(back_populates="medical_events")
    related_document: Mapped["Document | None"] = relationship()

    def __repr__(self) -> str:
        return f"<MedicalEvent {self.id} {self.event_type} {self.event_date}>"
