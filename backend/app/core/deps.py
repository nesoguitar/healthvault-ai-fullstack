"""
Shared FastAPI dependencies: DB session, current authenticated user,
and patient-scoped access control.

Every PHI-bearing endpoint depends on `get_current_user` (never trusts a
patient_id from the request path alone) and resolves the caller's own
Patient row server-side, so one account can never read another account's
records by guessing an id.
"""
import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.models.patient import Patient
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/auth/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    payload = decode_token(token)
    if payload is None or payload.get("type") != "access":
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    try:
        user = db.get(User, uuid.UUID(user_id))
    except (ValueError, TypeError):
        raise credentials_exception

    if user is None or not user.is_active:
        raise credentials_exception

    return user


def get_current_active_user(user: User = Depends(get_current_user)) -> User:
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user account")
    return user


def get_current_patient(
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Patient:
    """
    Resolve the Patient record owned by the authenticated user.

    All patient-data endpoints should depend on this rather than accepting
    a patient_id in the URL, which prevents IDOR-style access to other
    patients' PHI.
    """
    patient = db.query(Patient).filter(Patient.user_id == user.id).first()
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No patient profile found for this account",
        )
    return patient
