import uuid
from datetime import date

from pydantic import BaseModel, Field

from app.models.medication import MedicationStatus


class MedicationBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    generic_name: str | None = None
    dosage: str = Field(min_length=1, max_length=100)
    frequency: str = Field(min_length=1, max_length=100)
    route: str = Field(min_length=1, max_length=50)
    prescribed_by: str = Field(min_length=1, max_length=255)
    start_date: date
    end_date: date | None = None
    status: MedicationStatus = MedicationStatus.active
    purpose: str = Field(min_length=1, max_length=500)
    refills_remaining: int | None = Field(default=None, ge=0)
    instructions: str | None = None


class MedicationCreate(MedicationBase):
    pass


class MedicationUpdate(BaseModel):
    dosage: str | None = None
    frequency: str | None = None
    status: MedicationStatus | None = None
    end_date: date | None = None
    refills_remaining: int | None = Field(default=None, ge=0)
    instructions: str | None = None


class MedicationOut(MedicationBase):
    id: uuid.UUID
    patient_id: uuid.UUID

    model_config = {"from_attributes": True}
