import uuid
from datetime import date, datetime

from pydantic import BaseModel, Field

from app.models.medical_event import MedicalEventType


class MedicalEventBase(BaseModel):
    event_type: MedicalEventType
    event_date: date
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)
    provider: str | None = None
    facility: str | None = None
    tags: list[str] | None = None


class MedicalEventCreate(MedicalEventBase):
    related_document_id: uuid.UUID | None = None


class MedicalEventUpdate(BaseModel):
    event_type: MedicalEventType | None = None
    event_date: date | None = None
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    provider: str | None = None
    facility: str | None = None
    tags: list[str] | None = None


class MedicalEventOut(MedicalEventBase):
    id: uuid.UUID
    patient_id: uuid.UUID
    related_document_id: uuid.UUID | None
    created_at: datetime

    model_config = {"from_attributes": True}
