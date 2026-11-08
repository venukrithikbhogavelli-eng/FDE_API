from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_admin
from app.models.user import User
from app.schemas.user import UserUpdate, UserResponse, AdminUserUpdate
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])

DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]
AdminUser = Annotated[User, Depends(require_admin)]


# Admin: View all active, non-deleted users
@router.get("", response_model=list[UserResponse])
def get_all_users(db: DBSession, admin: AdminUser):
    return user_service.get_all_users_service(db)


# User: View own profile
# Admin: View any user's profile
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: DBSession, current_user: CurrentUser):
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own profile",
        )

    try:
        return user_service.get_user_service(db, user_id)

    except LookupError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


# Admin: Update user details, role and status
@router.patch("/{user_id}/admin", response_model=UserResponse)
def admin_update_user(
    user_id: int, user_data: AdminUserUpdate, db: DBSession, admin: AdminUser
):
    try:
        return user_service.admin_update_user_service(db, user_id, user_data)

    except LookupError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))

    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))


# Admin: Soft-delete user
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: DBSession, admin: AdminUser):
    try:
        user_service.soft_delete_user_service(db, user_id)

    except LookupError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


# Admin: View soft-deleted users
@router.get("/admin/deleted", response_model=list[UserResponse])
def get_deleted_users(db: DBSession, admin: AdminUser):
    return user_service.get_deleted_users_service(db)
