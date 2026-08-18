"""
Medical Timeline API — the chronological event feed shown on /timeline.

Soft-delete: DELETE marks `deleted_at` rather than removing the row, in
keeping with the record-retention rationale in app/models/mixins.py.
"""
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_patient
from app.models.medical_event import MedicalEvent, MedicalEventType
from app.models.patient import Patient
from app.schemas.medical_event import MedicalEventCreate, MedicalEventOut, MedicalEventUpdate

router = APIRouter()


@router.get("", response_model=list[MedicalEventOut])
def list_timeline_events(
    event_type: MedicalEventType | None = Query(default=None),
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    query = db.query(MedicalEvent).filter(
        MedicalEvent.patient_id == patient.id, MedicalEvent.deleted_at.is_(None)
    )
    if event_type:
        query = query.filter(MedicalEvent.event_type == event_type)
    return query.order_by(MedicalEvent.event_date.desc()).all()


@router.post("", response_model=MedicalEventOut, status_code=status.HTTP_201_CREATED)
def create_timeline_event(
    payload: MedicalEventCreate,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    event = MedicalEvent(patient_id=patient.id, **payload.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def _get_owned_event(db: Session, patient: Patient, event_id: uuid.UUID) -> MedicalEvent:
    event = (
        db.query(MedicalEvent)
        .filter(
            MedicalEvent.id == event_id,
            MedicalEvent.patient_id == patient.id,
            MedicalEvent.deleted_at.is_(None),
        )
        .first()
    )
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timeline event not found")
    return event


@router.get("/{event_id}", response_model=MedicalEventOut)
def get_timeline_event(
    event_id: uuid.UUID,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return _get_owned_event(db, patient, event_id)


@router.patch("/{event_id}", response_model=MedicalEventOut)
def update_timeline_event(
    event_id: uuid.UUID,
    payload: MedicalEventUpdate,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    event = _get_owned_event(db, patient, event_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(event, field, value)
    db.commit()
    db.refresh(event)
    return event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_timeline_event(
    event_id: uuid.UUID,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    event = _get_owned_event(db, patient, event_id)
    event.deleted_at = datetime.now(timezone.utc)
    db.commit()
