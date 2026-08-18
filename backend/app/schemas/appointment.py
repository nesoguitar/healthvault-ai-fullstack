import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.models.appointment import AppointmentStatus


class AppointmentBase(BaseModel):
    provider: str = Field(min_length=1, max_length=255)
    specialty: str = Field(min_length=1, max_length=255)
    facility: str = Field(min_length=1, max_length=255)
    scheduled_at: datetime
    reason: str = Field(min_length=1, max_length=500)
    location: str | None = None
    telehealth: bool = False


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    scheduled_at: datetime | None = None
    status: AppointmentStatus | None = None
    reason: str | None = None
    location: str | None = None


class AppointmentOut(AppointmentBase):
    id: uuid.UUID
    patient_id: uuid.UUID
    status: AppointmentStatus

    model_config = {"from_attributes": True}
