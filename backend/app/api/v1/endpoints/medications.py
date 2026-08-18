import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_patient
from app.models.medication import Medication
from app.models.patient import Patient
from app.schemas.medication import MedicationCreate, MedicationOut, MedicationUpdate

router = APIRouter()


@router.get("", response_model=list[MedicationOut])
def list_medications(patient: Patient = Depends(get_current_patient), db: Session = Depends(get_db)):
    return db.query(Medication).filter(Medication.patient_id == patient.id).order_by(Medication.start_date.desc()).all()


@router.post("", response_model=MedicationOut, status_code=status.HTTP_201_CREATED)
def create_medication(
    payload: MedicationCreate,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    medication = Medication(patient_id=patient.id, **payload.model_dump())
    db.add(medication)
    db.commit()
    db.refresh(medication)
    return medication


def _get_owned(db: Session, patient: Patient, medication_id: uuid.UUID) -> Medication:
    med = (
        db.query(Medication)
        .filter(Medication.id == medication_id, Medication.patient_id == patient.id)
        .first()
    )
    if med is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medication not found")
    return med


@router.patch("/{medication_id}", response_model=MedicationOut)
def update_medication(
    medication_id: uuid.UUID,
    payload: MedicationUpdate,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    med = _get_owned(db, patient, medication_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(med, field, value)
    db.commit()
    db.refresh(med)
    return med


@router.delete("/{medication_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medication(
    medication_id: uuid.UUID,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    med = _get_owned(db, patient, medication_id)
    db.delete(med)
    db.commit()
