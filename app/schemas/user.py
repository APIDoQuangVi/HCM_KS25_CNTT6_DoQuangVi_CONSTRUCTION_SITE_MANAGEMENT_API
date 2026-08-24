from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)

from app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "Họ tên không được để trống"
            )

        return value


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )


class UserUpdate(BaseModel):
    full_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    is_active: bool | None = None

    role: UserRole | None = None

    @field_validator("full_name")
    @classmethod
    def validate_full_name(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError(
                "Họ tên không được để trống"
            )

        return value


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