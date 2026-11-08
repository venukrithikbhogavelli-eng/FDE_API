from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

UserRole = Literal["admin", "user"]
UserStatus = Literal["active", "inactive"]


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(ge=18, le=100)
    role: UserRole = "user"
    status: UserStatus = "active"


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=18, le=100)
    status: UserStatus | None = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    role: UserRole
    status: UserStatus
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)


class AdminUserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=18, le=100)
    role: UserRole | None = None
    status: UserStatus | None = None
