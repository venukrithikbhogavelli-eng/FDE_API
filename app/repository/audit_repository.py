from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def create_audit_log(
    db: Session,
    actor_id: int | None,
    action: str,
    entity_type: str,
    entity_id: int | None = None,
    details: dict | None = None,
):
    audit_log = AuditLog(
        actor_id=actor_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        details=details,
    )

    try:
        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)
        return audit_log
    except Exception:
        db.rollback()
        raise


def get_audit_logs(db: Session):
    statement = select(AuditLog).order_by(AuditLog.created_at.desc())

    return list(db.scalars(statement).all())


def get_audit_logs_by_user(db: Session, actor_id: int):
    statement = (
        select(AuditLog)
        .where(AuditLog.actor_id == actor_id)
        .order_by(AuditLog.created_at.desc())
    )

    return list(db.scalars(statement).all())


def get_audit_logs_by_entity(db: Session, entity_type: str, entity_id: int):
    statement = (
        select(AuditLog)
        .where(AuditLog.entity_type == entity_type, AuditLog.entity_id == entity_id)
        .order_by(AuditLog.created_at.desc())
    )

    return list(db.scalars(statement).all())
