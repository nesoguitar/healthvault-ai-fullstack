import uuid
from datetime import date

from pydantic import BaseModel, Field

from app.models.allergy import AllergyCategory, AllergySeverity


class AllergyBase(BaseModel):
    allergen: str = Field(min_length=1, max_length=255)
    category: AllergyCategory
    reaction: str = Field(min_length=1, max_length=500)
    severity: AllergySeverity
    identified_date: date
    notes: str | None = None


class AllergyCreate(AllergyBase):
    pass


class AllergyUpdate(BaseModel):
    reaction: str | None = None
    severity: AllergySeverity | None = None
    notes: str | None = None


class AllergyOut(AllergyBase):
    id: uuid.UUID
    patient_id: uuid.UUID

    model_config = {"from_attributes": True}
