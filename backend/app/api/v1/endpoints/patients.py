"""
Patient profile + dashboard/summary endpoints.

Note there is no `/patients/{id}` route accepting an arbitrary id: every
route here resolves "the current user's own patient record" via
`get_current_patient`, which is the IDOR-prevention pattern used
throughout this API (see app/core/deps.py).
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_patient
from app.models.appointment import Appointment, AppointmentStatus
from app.models.diagnosis import Diagnosis
from app.models.document import Document
from app.models.lab_result import LabResult
from app.models.medication import Medication, MedicationStatus
from app.models.patient import Patient
from app.schemas.patient import PatientOut, PatientUpdate
from app.schemas.summary import DashboardSummary, HealthScore, HealthScoreCategory, PatientSummary

router = APIRouter()


@router.get("/me", response_model=PatientOut)
def get_my_patient_profile(patient: Patient = Depends(get_current_patient)):
    return patient


@router.patch("/me", response_model=PatientOut)
def update_my_patient_profile(
    payload: PatientUpdate,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(patient, field, value)
    db.commit()
    db.refresh(patient)
    return patient


def _compute_health_score(db: Session, patient: Patient) -> HealthScore:
    """
    Illustrative scoring — a real implementation would weigh lab flags,
    medication adherence signals, and preventive-care recency. Kept simple
    and transparent here so it's easy to replace with real clinical logic.
    """
    labs = db.query(LabResult).filter(LabResult.patient_id == patient.id).all()
    normal_labs = [l for l in labs if l.flag.value == "normal"]
    lab_score = round((len(normal_labs) / len(labs)) * 100) if labs else 100

    active_meds = (
        db.query(Medication)
        .filter(Medication.patient_id == patient.id, Medication.status == MedicationStatus.active)
        .count()
    )
    adherence_score = 94 if active_meds else 100

    categories = [
        HealthScoreCategory(label="Vitals", score=88, trend="flat"),
        HealthScoreCategory(label="Labs", score=lab_score, trend="up"),
        HealthScoreCategory(label="Medication adherence", score=adherence_score, trend="flat"),
        HealthScoreCategory(label="Preventive care", score=76, trend="up"),
    ]
    overall = round(sum(c.score for c in categories) / len(categories))
    return HealthScore(overall=overall, categories=categories)


@router.get("/me/summary", response_model=PatientSummary)
def get_my_summary(patient: Patient = Depends(get_current_patient), db: Session = Depends(get_db)):
    return PatientSummary(
        patient=patient,
        diagnoses=db.query(Diagnosis).filter(Diagnosis.patient_id == patient.id).all(),
        medications=db.query(Medication).filter(Medication.patient_id == patient.id).all(),
        allergies=patient.allergies,
        recent_labs=(
            db.query(LabResult)
            .filter(LabResult.patient_id == patient.id)
            .order_by(LabResult.result_date.desc())
            .limit(10)
            .all()
        ),
    )


@router.get("/me/dashboard", response_model=DashboardSummary)
def get_my_dashboard(patient: Patient = Depends(get_current_patient), db: Session = Depends(get_db)):
    active_conditions = (
        db.query(Diagnosis)
        .filter(Diagnosis.patient_id == patient.id, Diagnosis.status.in_(["active", "chronic"]))
        .all()
    )
    current_medications = (
        db.query(Medication)
        .filter(Medication.patient_id == patient.id, Medication.status == MedicationStatus.active)
        .all()
    )
    recent_labs = (
        db.query(LabResult)
        .filter(LabResult.patient_id == patient.id)
        .order_by(LabResult.result_date.desc())
        .limit(4)
        .all()
    )
    upcoming_appointments = (
        db.query(Appointment)
        .filter(Appointment.patient_id == patient.id, Appointment.status == AppointmentStatus.scheduled)
        .order_by(Appointment.scheduled_at.asc())
        .limit(3)
        .all()
    )
    recent_documents = (
        db.query(Document)
        .filter(Document.patient_id == patient.id, Document.deleted_at.is_(None))
        .order_by(Document.uploaded_at.desc())
        .limit(4)
        .all()
    )

    return DashboardSummary(
        patient=patient,
        health_score=_compute_health_score(db, patient),
        active_conditions=active_conditions,
        current_medications=current_medications,
        recent_labs=recent_labs,
        upcoming_appointments=upcoming_appointments,
        recent_documents=recent_documents,
    )
