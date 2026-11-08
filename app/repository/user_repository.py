from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def create_registered_user(db: Session, user_data, hashed_password: str):
    user = User(
        name=user_data.name,
        email=str(user_data.email),
        age=user_data.age,
        password_hash=hashed_password,
        role="user",
        status="active",
        is_deleted=False,
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        raise


def get_user_by_id(db: Session, user_id: int):
    statement = select(User).where(User.id == user_id, User.is_deleted.is_(False))
    return db.scalar(statement)


def get_user_by_email(db: Session, email: str):
    statement = select(User).where(User.email == email, User.is_deleted.is_(False))
    return db.scalar(statement)


def get_user_for_authentication(db: Session, email: str):
    statement = select(User).where(User.email == email)
    return db.scalar(statement)


def get_all_users(db: Session):
    statement = select(User).where(User.is_deleted.is_(False)).order_by(User.id)
    return list(db.scalars(statement).all())


def update_user(db: Session, user: User, user_data: UserUpdate):
    update_data = user_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if field == "email" and value is not None:
            value = str(value)

        setattr(user, field, value)

    try:
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        raise


def update_user_status(db: Session, user: User, status: str):
    user.status = status
    user.updated_at = datetime.now(timezone.utc)

    try:
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        raise


def soft_delete_user(db: Session, user: User):
    user.is_deleted = True
    user.status = "inactive"
    user.deleted_at = datetime.now(timezone.utc)
    user.updated_at = datetime.now(timezone.utc)

    try:
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        raise


def get_deleted_users(db: Session):
    statement = select(User).where(User.is_deleted.is_(True)).order_by(User.id)
    return list(db.scalars(statement).all())
