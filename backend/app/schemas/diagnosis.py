import uuid
from datetime import date

from pydantic import BaseModel, Field

from app.models.diagnosis import DiagnosisSeverity, DiagnosisStatus


class DiagnosisBase(BaseModel):
    condition: str = Field(min_length=1, max_length=255)
    icd10_code: str = Field(min_length=1, max_length=20)
    diagnosed_date: date
    status: DiagnosisStatus
    severity: DiagnosisSeverity
    diagnosed_by: str = Field(min_length=1, max_length=255)
    notes: str | None = None


class DiagnosisCreate(DiagnosisBase):
    pass


class DiagnosisUpdate(BaseModel):
    status: DiagnosisStatus | None = None
    severity: DiagnosisSeverity | None = None
    notes: str | None = None


class DiagnosisOut(DiagnosisBase):
    id: uuid.UUID
    patient_id: uuid.UUID

    model_config = {"from_attributes": True}
