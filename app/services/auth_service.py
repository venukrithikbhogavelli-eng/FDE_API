from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.repository import user_repository
from app.schemas.auth import UserRegister


def register_user_service(db: Session, user_data: UserRegister):
    email = str(user_data.email)

    existing_user = user_repository.get_user_for_authentication(db, email)

    if existing_user:
        raise ValueError("Email already registered")

    hashed_password = hash_password(user_data.password)

    user = user_repository.create_registered_user(db, user_data, hashed_password)

    return user


def login_user_service(db: Session, email: str, password: str):
    user = user_repository.get_user_for_authentication(db, email)

    if not user or not user.password_hash:
        raise ValueError("Invalid email or password")

    if not verify_password(password, user.password_hash):
        raise ValueError("Invalid email or password")

    if user.is_deleted:
        raise ValueError("Account is unavailable")

    if user.status != "active":
        raise ValueError("Account is inactive")

    access_token = create_access_token(user_id=user.id, role=user.role)

    return {"access_token": access_token, "token_type": "bearer", "expires_in": 30 * 60}
