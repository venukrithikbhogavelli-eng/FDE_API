from sqlalchemy.orm import Session

from app.repository import audit_repository


def record_audit_event(
    db: Session,
    actor_id: int | None,
    action: str,
    entity_type: str,
    entity_id: int | None = None,
    details: dict | None = None,
):
    return audit_repository.create_audit_log(
        db=db,
        actor_id=actor_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        details=details,
    )


def get_all_audit_logs_service(db: Session):
    return audit_repository.get_audit_logs(db)


def get_user_audit_logs_service(db: Session, actor_id: int):
    return audit_repository.get_audit_logs_by_user(db, actor_id)


def get_entity_audit_logs_service(db: Session, entity_type: str, entity_id: int):
    return audit_repository.get_audit_logs_by_entity(db, entity_type, entity_id)
