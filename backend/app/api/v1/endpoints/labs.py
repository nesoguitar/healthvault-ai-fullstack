"""
Lab Results API, including the /labs/trends/{test_name} endpoint that backs
the trend charts on /summary — a lightweight analog to the frontend's
mocked `history` array, computed here from real historical rows instead.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_patient
from app.models.lab_result import LabResult
from app.models.patient import Patient
from app.schemas.lab_result import (
    LabResultCreate,
    LabResultHistoryPoint,
    LabResultOut,
    LabResultTrend,
)

router = APIRouter()


@router.get("", response_model=list[LabResultOut])
def list_lab_results(patient: Patient = Depends(get_current_patient), db: Session = Depends(get_db)):
    return (
        db.query(LabResult)
        .filter(LabResult.patient_id == patient.id)
        .order_by(LabResult.result_date.desc())
        .all()
    )


@router.post("", response_model=LabResultOut, status_code=status.HTTP_201_CREATED)
def create_lab_result(
    payload: LabResultCreate,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    lab = LabResult(patient_id=patient.id, **payload.model_dump())
    db.add(lab)
    db.commit()
    db.refresh(lab)
    return lab


@router.get("/trends/{test_name}", response_model=LabResultTrend)
def get_lab_trend(
    test_name: str,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(LabResult)
        .filter(LabResult.patient_id == patient.id, LabResult.test_name == test_name)
        .order_by(LabResult.result_date.asc())
        .all()
    )
    if not rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found for this test")

    return LabResultTrend(
        test_name=test_name,
        unit=rows[-1].unit,
        reference_range=rows[-1].reference_range,
        history=[LabResultHistoryPoint(result_date=r.result_date, value=r.value) for r in rows],
    )
