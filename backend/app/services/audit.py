"""
Audit logging helper. Call `record()` from endpoints (or the middleware in
app/main.py) whenever PHI is created, read, updated, or deleted.
"""
import uuid

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.audit_log import AuditLog


def record(
    db: Session,
    *,
    actor_user_id: uuid.UUID | None,
    actor_ip: str | None,
    action: str,
    resource_type: str,
    resource_id: str | None,
    status_code: int,
    detail: str | None = None,
) -> None:
    if not settings.AUDIT_LOG_ENABLED:
        return
    entry = AuditLog(
        actor_user_id=actor_user_id,
        actor_ip=actor_ip,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        status_code=status_code,
        detail=detail,
    )
    db.add(entry)
    db.commit()
