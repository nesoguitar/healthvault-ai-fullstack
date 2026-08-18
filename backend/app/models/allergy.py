import enum
import uuid
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class AllergyCategory(str, enum.Enum):
    medication = "medication"
    food = "food"
    environmental = "environmental"
    other = "other"


class AllergySeverity(str, enum.Enum):
    mild = "mild"
    moderate = "moderate"
    severe = "severe"
    life_threatening = "life_threatening"


class Allergy(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "allergies"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True
    )

    allergen: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[AllergyCategory] = mapped_column(
        Enum(AllergyCategory, name="allergy_category_enum"), nullable=False
    )
    reaction: Mapped[str] = mapped_column(String(500), nullable=False)
    severity: Mapped[AllergySeverity] = mapped_column(
        Enum(AllergySeverity, name="allergy_severity_enum"), nullable=False, index=True
    )
    identified_date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    patient: Mapped["Patient"] = relationship(back_populates="allergies")

    def __repr__(self) -> str:
        return f"<Allergy {self.id} {self.allergen}>"
