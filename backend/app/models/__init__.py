"""
Import every model here so that:
1. `Base.metadata` sees all tables (needed for Alembic autogenerate).
2. SQLAlchemy can resolve string-based relationship() references between
   modules regardless of import order.
"""
from app.models.allergy import Allergy  # noqa: F401
from app.models.appointment import Appointment  # noqa: F401
from app.models.audit_log import AuditLog  # noqa: F401
from app.models.chat import ChatMessage, ChatSession  # noqa: F401
from app.models.diagnosis import Diagnosis  # noqa: F401
from app.models.document import Document  # noqa: F401
from app.models.lab_result import LabResult  # noqa: F401
from app.models.medical_event import MedicalEvent  # noqa: F401
from app.models.medication import Medication  # noqa: F401
from app.models.patient import Patient  # noqa: F401
from app.models.user import User  # noqa: F401

__all__ = [
    "Allergy",
    "Appointment",
    "AuditLog",
    "ChatMessage",
    "ChatSession",
    "Diagnosis",
    "Document",
    "LabResult",
    "MedicalEvent",
    "Medication",
    "Patient",
    "User",
]
