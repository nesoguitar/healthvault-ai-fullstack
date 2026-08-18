import uuid
from datetime import date

from pydantic import BaseModel, Field

from app.models.lab_result import LabFlag


class LabResultBase(BaseModel):
    test_name: str = Field(min_length=1, max_length=255)
    category: str = Field(min_length=1, max_length=100)
    value: float
    unit: str = Field(min_length=1, max_length=50)
    reference_range: str = Field(min_length=1, max_length=100)
    flag: LabFlag
    result_date: date
    ordered_by: str = Field(min_length=1, max_length=255)


class LabResultCreate(LabResultBase):
    source_document_id: uuid.UUID | None = None


class LabResultOut(LabResultBase):
    id: uuid.UUID
    patient_id: uuid.UUID
    source_document_id: uuid.UUID | None

    model_config = {"from_attributes": True}


class LabResultHistoryPoint(BaseModel):
    result_date: date
    value: float


class LabResultTrend(BaseModel):
    test_name: str
    unit: str
    reference_range: str
    history: list[LabResultHistoryPoint]
