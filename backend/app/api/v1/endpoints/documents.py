"""
File Upload API.

Flow:
1. Client uploads a file -> validated (extension, size) -> streamed to
   storage (local disk or Azure Blob) -> a Document row is created with
   status="processing" and returned immediately (202-style UX, 201 status).
2. A background task extracts text (Azure Document Intelligence, or a
   no-op stub locally), generates an embedding, and flips status to
   "processed" or "failed". The frontend polls GET /documents or
   GET /documents/{id} to observe the status transition, matching the
   upload dropzone's uploading -> success/error states.
"""
import uuid
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal, get_db
from app.core.deps import get_current_patient
from app.models.document import Document, DocumentFileType, DocumentStatus, DocumentType
from app.models.patient import Patient
from app.schemas.document import DocumentOut, DocumentUploadResponse
from app.services.ai import get_ai_provider
from app.services.document_intelligence import get_document_extractor
from app.services.storage import get_storage_backend, sha256_hex

router = APIRouter()

EXT_TO_FILE_TYPE = {
    ".pdf": DocumentFileType.pdf,
    ".jpg": DocumentFileType.jpg,
    ".jpeg": DocumentFileType.jpg,
    ".png": DocumentFileType.png,
}
EXT_TO_CONTENT_TYPE = {
    ".pdf": "application/pdf",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
}


def _process_document(document_id: uuid.UUID) -> None:
    """
    Runs in a FastAPI BackgroundTask (in-process, after the response has
    been sent). For production throughput/reliability, replace this with a
    durable queue (Azure Service Bus / Celery) so processing survives a
    process restart — the function body itself would be unchanged.
    """
    db = SessionLocal()
    try:
        document = db.get(Document, document_id)
        if document is None:
            return
        try:
            storage = get_storage_backend()
            content = storage.read(document.storage_key)

            extractor = get_document_extractor()
            content_type = EXT_TO_CONTENT_TYPE.get(Path(document.file_name).suffix.lower(), "application/pdf")
            result = extractor.extract(content, content_type)

            document.extracted_text = result.text or None
            document.summary = result.summary or (result.text[:280] if result.text else None)

            if result.text:
                ai = get_ai_provider()
                document.embedding = ai.embed(result.text[:8000])

            document.status = DocumentStatus.processed
        except Exception as exc:  # noqa: BLE001 — surfaced via processing_error, not raised
            document.status = DocumentStatus.failed
            document.processing_error = str(exc)
        db.commit()
    finally:
        db.close()


@router.get("", response_model=list[DocumentOut])
def list_documents(patient: Patient = Depends(get_current_patient), db: Session = Depends(get_db)):
    return (
        db.query(Document)
        .filter(Document.patient_id == patient.id, Document.deleted_at.is_(None))
        .order_by(Document.uploaded_at.desc())
        .all()
    )


@router.post("", response_model=DocumentUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile,
    background_tasks: BackgroundTasks,
    document_type: DocumentType = DocumentType.other,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    ext = Path(file.filename or "").suffix.lower()
    if ext not in settings.ALLOWED_UPLOAD_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(settings.ALLOWED_UPLOAD_EXTENSIONS)}",
        )

    content = await file.read()
    size_kb = len(content) // 1024
    if size_kb > settings.MAX_UPLOAD_SIZE_MB * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds the {settings.MAX_UPLOAD_SIZE_MB}MB limit",
        )

    storage = get_storage_backend()
    storage_key = storage.save(patient_id=str(patient.id), file_name=file.filename or "upload", content=content)

    document = Document(
        patient_id=patient.id,
        file_name=file.filename or "upload",
        document_type=document_type,
        file_type=EXT_TO_FILE_TYPE[ext],
        size_kb=size_kb,
        storage_backend=settings.STORAGE_BACKEND,
        storage_key=storage_key,
        content_hash=sha256_hex(content),
        status=DocumentStatus.processing,
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    background_tasks.add_task(_process_document, document.id)

    return DocumentUploadResponse(document=document)


def _get_owned(db: Session, patient: Patient, document_id: uuid.UUID) -> Document:
    document = (
        db.query(Document)
        .filter(Document.id == document_id, Document.patient_id == patient.id, Document.deleted_at.is_(None))
        .first()
    )
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return document


@router.get("/{document_id}", response_model=DocumentOut)
def get_document(
    document_id: uuid.UUID,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return _get_owned(db, patient, document_id)


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: uuid.UUID,
    patient: Patient = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    from datetime import datetime, timezone

    document = _get_owned(db, patient, document_id)
    document.deleted_at = datetime.now(timezone.utc)
    db.commit()
