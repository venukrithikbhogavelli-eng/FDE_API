from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func

from app.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    __table_args__ = {"schema": "fde"}

    id = Column(Integer, primary_key=True, index=True)

    actor_id = Column(Integer, ForeignKey("fde.users.id"), nullable=True)

    action = Column(String(100), nullable=False)

    entity_type = Column(String(100), nullable=False)

    entity_id = Column(Integer, nullable=True)

    details = Column(JSON, nullable=True)

    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
