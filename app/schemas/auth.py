from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
)


class RegisterRequest(BaseModel):
    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )

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


class LoginRequest(BaseModel):
    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"