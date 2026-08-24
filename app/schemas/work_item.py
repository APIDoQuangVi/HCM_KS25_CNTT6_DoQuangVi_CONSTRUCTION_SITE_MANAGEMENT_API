from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.work_item import WorkItemPriority, WorkItemStatus


class WorkItemBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    assignee_id: int | None = Field(default=None, gt=0)
    status: WorkItemStatus = WorkItemStatus.TODO
    priority: WorkItemPriority = WorkItemPriority.MEDIUM
    due_date: datetime | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError("Tiêu đề hạng mục không được để trống")

        return value


class WorkItemCreate(WorkItemBase):
    pass


class WorkItemUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    description: str | None = None

    assignee_id: int | None = Field(
        default=None,
        gt=0
    )

    status: WorkItemStatus | None = None
    priority: WorkItemPriority | None = None
    due_date: datetime | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str | None):
        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError("Tiêu đề hạng mục không được để trống")

        return value


class WorkItemResponse(WorkItemBase):
    id: int
    site_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )