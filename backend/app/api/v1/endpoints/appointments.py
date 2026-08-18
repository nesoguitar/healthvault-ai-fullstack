import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_patient
from app.models.appointment import Appointment
from app.models.patient import Patient
from app.schemas.appointment import AppointmentCreate, AppointmentOut, AppointmentUpdate

router = APIRouter()


@router.get("", response_model=list[AppointmentOut])
def list_appointments(patient: Patient = Depends(get_current_patient), db: Session = Depends(get_db)):
    return (
        db.query(Appointment)
        .filter(Appointment.patient_id == patient.id)
        .order_by(Appointment.scheduled_at.desc())
        .all()
    )


@router.post("", response_model=AppointmentOut, status_code=status.HTTP_201_CREATED)
def create_appointment(
    payload: AppointmentCreate,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    appointment = Appointment(patient_id=patient.id, **payload.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


def _get_owned(db: Session, patient: Patient, appointment_id: uuid.UUID) -> Appointment:
    appt = (
        db.query(Appointment)
        .filter(Appointment.id == appointment_id, Appointment.patient_id == patient.id)
        .first()
    )
    if appt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return appt


@router.patch("/{appointment_id}", response_model=AppointmentOut)
def update_appointment(
    appointment_id: uuid.UUID,
    payload: AppointmentUpdate,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    appt = _get_owned(db, patient, appointment_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(appt, field, value)
    db.commit()
    db.refresh(appt)
    return appt


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(
    appointment_id: uuid.UUID,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    appt = _get_owned(db, patient, appointment_id)
    db.delete(appt)
    db.commit()
