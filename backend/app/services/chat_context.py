"""
Builds the grounding context for the AI chat endpoint from the patient's
own structured records — this is what keeps answers from being generic
model knowledge instead of *this patient's* data.

For the mock/dev provider this context is unused; for real providers it is
injected as a system message (see app/services/ai.py) so the model must
answer from these facts rather than training data.
"""
from sqlalchemy.orm import Session

from app.models.allergy import Allergy
from app.models.diagnosis import Diagnosis
from app.models.lab_result import LabResult
from app.models.medical_event import MedicalEvent
from app.models.medication import Medication
from app.models.patient import Patient


def build_patient_context(db: Session, patient: Patient, max_events: int = 15) -> str:
    diagnoses = db.query(Diagnosis).filter(Diagnosis.patient_id == patient.id).all()
    medications = (
        db.query(Medication)
        .filter(Medication.patient_id == patient.id, Medication.status == "active")
        .all()
    )
    allergies = db.query(Allergy).filter(Allergy.patient_id == patient.id).all()
    labs = (
        db.query(LabResult)
        .filter(LabResult.patient_id == patient.id)
        .order_by(LabResult.result_date.desc())
        .limit(10)
        .all()
    )
    events = (
        db.query(MedicalEvent)
        .filter(MedicalEvent.patient_id == patient.id, MedicalEvent.deleted_at.is_(None))
        .order_by(MedicalEvent.event_date.desc())
        .limit(max_events)
        .all()
    )

    lines: list[str] = [f"Patient: {patient.first_name} {patient.last_name}, DOB {patient.date_of_birth}"]

    lines.append("\nActive/chronic conditions:")
    for d in diagnoses:
        lines.append(f"- {d.condition} ({d.icd10_code}), status={d.status.value}, diagnosed {d.diagnosed_date}")

    lines.append("\nCurrent medications:")
    for m in medications:
        lines.append(f"- {m.name} {m.dosage}, {m.frequency}, for {m.purpose}")

    lines.append("\nAllergies:")
    for a in allergies:
        lines.append(f"- {a.allergen} ({a.severity.value}): {a.reaction}")

    lines.append("\nRecent lab results:")
    for lab in labs:
        lines.append(f"- {lab.test_name}: {lab.value} {lab.unit} on {lab.result_date} (flag={lab.flag.value})")

    lines.append("\nRecent timeline events:")
    for e in events:
        lines.append(f"- {e.event_date}: [{e.event_type.value}] {e.title} — {e.description}")

    return "\n".join(lines)
