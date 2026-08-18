import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_patient
from app.models.diagnosis import Diagnosis
from app.models.patient import Patient
from app.schemas.diagnosis import DiagnosisCreate, DiagnosisOut, DiagnosisUpdate

router = APIRouter()


@router.get("", response_model=list[DiagnosisOut])
def list_diagnoses(patient: Patient = Depends(get_current_patient), db: Session = Depends(get_db)):
    return (
        db.query(Diagnosis)
        .filter(Diagnosis.patient_id == patient.id)
        .order_by(Diagnosis.diagnosed_date.desc())
        .all()
    )


@router.post("", response_model=DiagnosisOut, status_code=status.HTTP_201_CREATED)
def create_diagnosis(
    payload: DiagnosisCreate,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    diagnosis = Diagnosis(patient_id=patient.id, **payload.model_dump())
    db.add(diagnosis)
    db.commit()
    db.refresh(diagnosis)
    return diagnosis


def _get_owned(db: Session, patient: Patient, diagnosis_id: uuid.UUID) -> Diagnosis:
    dx = (
        db.query(Diagnosis)
        .filter(Diagnosis.id == diagnosis_id, Diagnosis.patient_id == patient.id)
        .first()
    )
    if dx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diagnosis not found")
    return dx


@router.patch("/{diagnosis_id}", response_model=DiagnosisOut)
def update_diagnosis(
    diagnosis_id: uuid.UUID,
    payload: DiagnosisUpdate,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    dx = _get_owned(db, patient, diagnosis_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(dx, field, value)
    db.commit()
    db.refresh(dx)
    return dx


@router.delete("/{diagnosis_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_diagnosis(
    diagnosis_id: uuid.UUID,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    dx = _get_owned(db, patient, diagnosis_id)
    db.delete(dx)
    db.commit()
