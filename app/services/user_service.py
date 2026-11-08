from sqlalchemy.orm import Session

from app.repository import user_repository
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.user import UserCreate, UserUpdate, AdminUserUpdate

def create_user_service(db: Session, user_data: UserCreate):
    existing_user = user_repository.get_user_for_authentication(
        db, str(user_data.email)
    )

    if existing_user:
        raise ValueError("Email already registered")

    return user_repository.create_user(db, user_data)


def get_user_service(db: Session, user_id: int):
    user = user_repository.get_user_by_id(db, user_id)

    if not user:
        raise LookupError("User not found")

    return user


def get_all_users_service(db: Session):
    return user_repository.get_all_users(db)


def update_user_service(db: Session, user_id: int, user_data: UserUpdate):
    user = user_repository.get_user_by_id(db, user_id)

    if not user:
        raise LookupError("User not found")

    if user_data.email is not None:
        existing_user = user_repository.get_user_for_authentication(
            db, str(user_data.email)
        )

        if existing_user and existing_user.id != user_id:
            raise ValueError("Email already registered")

    return user_repository.update_user(db, user, user_data)


def update_user_status_service(db: Session, user_id: int, status: str):
    if status not in ("active", "inactive"):
        raise ValueError("Invalid account status")

    user = user_repository.get_user_by_id(db, user_id)

    if not user:
        raise LookupError("User not found")

    return user_repository.update_user_status(db, user, status)


def soft_delete_user_service(db: Session, user_id: int):
    user = user_repository.get_user_by_id(db, user_id)

    if not user:
        raise LookupError("User not found")

    return user_repository.soft_delete_user(db, user)


def get_deleted_users_service(db: Session):
    return user_repository.get_deleted_users(db)


def admin_update_user_service(db: Session, user_id: int, user_data: AdminUserUpdate):
    user = user_repository.get_user_by_id(db, user_id)

    if not user:
        raise LookupError("User not found")

    if user_data.email is not None:
        existing_user = user_repository.get_user_for_authentication(
            db, str(user_data.email)
        )

        if existing_user and existing_user.id != user_id:
            raise ValueError("Email already registered")

    update_data = user_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if field == "email":
            value = str(value)

        setattr(user, field, value)

    try:
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        raise
