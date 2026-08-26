from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)

from app.models.work_item import (
    WorkItemPriority,
    WorkItemStatus,
)


class WorkItemBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        max_length=2000,
    )

    assignee_id: int | None = None

    status: WorkItemStatus = WorkItemStatus.TODO

    priority: WorkItemPriority = WorkItemPriority.MEDIUM

    due_date: datetime | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "Tên hạng mục không được để trống"
            )

        return value

    @field_validator("description")
    @classmethod
    def validate_description(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            return None

        return value


class WorkItemCreate(WorkItemBase):
    pass


class WorkItemUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        max_length=2000,
    )

    assignee_id: int | None = None

    status: WorkItemStatus | None = None

    priority: WorkItemPriority | None = None

    due_date: datetime | None = None

    @field_validator("title")
    @classmethod
    def validate_title(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError(
                "Tên hạng mục không được để trống"
            )

        return value

    @field_validator("description")
    @classmethod
    def validate_description(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            return None

        return value


class WorkItemResponse(WorkItemBase):
    id: int
    site_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class WorkItemPaginatedResponse(BaseModel):
    items: list[WorkItemResponse]
    totalpage: int
    page: int
    total: int
    size: int