import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_patient
from app.models.allergy import Allergy
from app.models.patient import Patient
from app.schemas.allergy import AllergyCreate, AllergyOut, AllergyUpdate

router = APIRouter()


@router.get("", response_model=list[AllergyOut])
def list_allergies(patient: Patient = Depends(get_current_patient), db: Session = Depends(get_db)):
    return db.query(Allergy).filter(Allergy.patient_id == patient.id).all()


@router.post("", response_model=AllergyOut, status_code=status.HTTP_201_CREATED)
def create_allergy(
    payload: AllergyCreate,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    allergy = Allergy(patient_id=patient.id, **payload.model_dump())
    db.add(allergy)
    db.commit()
    db.refresh(allergy)
    return allergy


def _get_owned(db: Session, patient: Patient, allergy_id: uuid.UUID) -> Allergy:
    allergy = db.query(Allergy).filter(Allergy.id == allergy_id, Allergy.patient_id == patient.id).first()
    if allergy is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Allergy not found")
    return allergy


@router.patch("/{allergy_id}", response_model=AllergyOut)
def update_allergy(
    allergy_id: uuid.UUID,
    payload: AllergyUpdate,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    allergy = _get_owned(db, patient, allergy_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(allergy, field, value)
    db.commit()
    db.refresh(allergy)
    return allergy


@router.delete("/{allergy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_allergy(
    allergy_id: uuid.UUID,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    allergy = _get_owned(db, patient, allergy_id)
    db.delete(allergy)
    db.commit()
