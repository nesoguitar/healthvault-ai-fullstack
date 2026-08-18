import uuid
from datetime import date

from pydantic import BaseModel, Field

from app.models.patient import Sex


class PatientBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    date_of_birth: date
    sex: Sex = Sex.unspecified
    phone: str | None = None
    address: str | None = None
    blood_type: str | None = Field(default=None, max_length=5)
    height_cm: float | None = Field(default=None, gt=0, lt=300)
    weight_kg: float | None = Field(default=None, gt=0, lt=500)


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    phone: str | None = None
    address: str | None = None
    blood_type: str | None = Field(default=None, max_length=5)
    height_cm: float | None = Field(default=None, gt=0, lt=300)
    weight_kg: float | None = Field(default=None, gt=0, lt=500)


class PatientOut(PatientBase):
    id: uuid.UUID
    user_id: uuid.UUID

    model_config = {"from_attributes": True}
