from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ConstructionSiteBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
    )
    


    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "Tên công trình không được để trống"
            )

        return value

    @field_validator("description")
    @classmethod
    def validate_description(
        cls,
        value: Optional[str],
    ) -> Optional[str]:
        if value is None:
            return None

        value = value.strip()

        if not value:
            return None

        return value


class ConstructionSiteCreate(ConstructionSiteBase):
    pass


class ConstructionSiteUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError(
                "Tên công trình không được để trống"
            )

        return value

    @field_validator("description")
    @classmethod
    def validate_description(
        cls,
        value: Optional[str],
    ) -> Optional[str]:
        if value is None:
            return None

        value = value.strip()

        if not value:
            return None

        return value


class ConstructionSiteResponse(ConstructionSiteBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )