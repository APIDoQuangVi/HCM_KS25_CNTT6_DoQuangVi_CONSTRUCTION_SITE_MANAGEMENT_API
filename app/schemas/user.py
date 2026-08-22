from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: str | None = None
    is_active: bool | None = None
    role: UserRole | None = None


class UserResponse(BaseModel):

    id: int

    email: str

    full_name: str

    role: UserRole

    is_active: bool

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
