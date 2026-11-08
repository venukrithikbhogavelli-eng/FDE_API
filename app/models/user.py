from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Integer,
    String,
    text,
)
from sqlalchemy.sql import func

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        CheckConstraint("role IN ('admin', 'user')", name="ck_users_role"),
        CheckConstraint("status IN ('active', 'inactive')", name="ck_users_status"),
        {"schema": "fde"},
    )

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)

    age = Column(Integer, nullable=False)

    password_hash = Column(String(255), nullable=True)

    role = Column(
        String(20), nullable=False, default="user", server_default=text("'user'")
    )

    status = Column(
        String(20), nullable=False, default="active", server_default=text("'active'")
    )

    is_deleted = Column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )

    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    deleted_at = Column(DateTime(timezone=True), nullable=True)
