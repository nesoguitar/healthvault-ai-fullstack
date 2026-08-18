import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.document import DocumentFileType, DocumentStatus, DocumentType


class DocumentOut(BaseModel):
    id: uuid.UUID
    patient_id: uuid.UUID
    file_name: str
    document_type: DocumentType
    file_type: DocumentFileType
    size_kb: int
    status: DocumentStatus
    summary: str | None
    uploaded_at: datetime

    model_config = {"from_attributes": True}


class DocumentUploadResponse(BaseModel):
    document: DocumentOut
    message: str = "File accepted and queued for processing."


class DocumentUpdate(BaseModel):
    document_type: DocumentType | None = None
