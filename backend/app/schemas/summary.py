"""Aggregate schemas that back dashboard/summary-style endpoints."""
from app.schemas.allergy import AllergyOut
from app.schemas.appointment import AppointmentOut
from app.schemas.diagnosis import DiagnosisOut
from app.schemas.document import DocumentOut
from app.schemas.lab_result import LabResultOut
from app.schemas.medication import MedicationOut
from app.schemas.patient import PatientOut
from pydantic import BaseModel


class HealthScoreCategory(BaseModel):
    label: str
    score: int
    trend: str  # "up" | "down" | "flat"


class HealthScore(BaseModel):
    overall: int
    categories: list[HealthScoreCategory]


class PatientSummary(BaseModel):
    patient: PatientOut
    diagnoses: list[DiagnosisOut]
    medications: list[MedicationOut]
    allergies: list[AllergyOut]
    recent_labs: list[LabResultOut]


class DashboardSummary(BaseModel):
    patient: PatientOut
    health_score: HealthScore
    active_conditions: list[DiagnosisOut]
    current_medications: list[MedicationOut]
    recent_labs: list[LabResultOut]
    upcoming_appointments: list[AppointmentOut]
    recent_documents: list[DocumentOut]
