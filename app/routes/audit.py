from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_admin
from app.models.user import User
from app.schemas.audit import AuditLogResponse
from app.services import audit_service

router = APIRouter(prefix="/audit", tags=["Audit Logs"])

DBSession = Annotated[Session, Depends(get_db)]
AdminUser = Annotated[User, Depends(require_admin)]


# Admin: Retrieve all audit logs
@router.get("", response_model=list[AuditLogResponse])
def get_all_audit_logs(db: DBSession, admin: AdminUser):
    return audit_service.get_all_audit_logs_service(db)


# Admin: Retrieve audit logs performed by a specific user
@router.get("/user/{actor_id}", response_model=list[AuditLogResponse])
def get_user_audit_logs(actor_id: int, db: DBSession, admin: AdminUser):
    return audit_service.get_user_audit_logs_service(db, actor_id)


# Admin: Retrieve history of a specific entity
@router.get("/entity/{entity_type}/{entity_id}", response_model=list[AuditLogResponse])
def get_entity_audit_logs(
    entity_type: str, entity_id: int, db: DBSession, admin: AdminUser
):
    return audit_service.get_entity_audit_logs_service(db, entity_type, entity_id)
