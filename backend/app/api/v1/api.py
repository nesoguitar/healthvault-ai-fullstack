from fastapi import APIRouter

from app.api.v1.endpoints import (
    allergies,
    appointments,
    auth,
    chat,
    diagnoses,
    documents,
    labs,
    medications,
    patients,
    timeline,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(patients.router, prefix="/patients", tags=["Patient"])
api_router.include_router(timeline.router, prefix="/timeline", tags=["Medical Timeline"])
api_router.include_router(medications.router, prefix="/medications", tags=["Medications"])
api_router.include_router(diagnoses.router, prefix="/diagnoses", tags=["Diagnoses"])
api_router.include_router(allergies.router, prefix="/allergies", tags=["Allergies"])
api_router.include_router(labs.router, prefix="/labs", tags=["Lab Results"])
api_router.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
api_router.include_router(chat.router, prefix="/chat", tags=["AI Chat"])
