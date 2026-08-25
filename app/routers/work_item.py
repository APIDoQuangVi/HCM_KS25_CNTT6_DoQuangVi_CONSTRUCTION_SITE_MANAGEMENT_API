from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.work_item import (
    WorkItemPriority,
    WorkItemStatus,
)
from app.schemas.work_item import (
    WorkItemCreate,
    WorkItemResponse,
    WorkItemUpdate,
)
from app.services import work_item_service


router = APIRouter(
    tags=["Work Items"],
)


@router.post(
    "/construction-sites/{site_id}/work-items",
    response_model=WorkItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_work_item(
    site_id: int,
    item_data: WorkItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return work_item_service.create_work_item(
        db,
        site_id,
        item_data,
        current_user,
    )


@router.get(
    "/construction-sites/{site_id}/work-items",
    response_model=list[WorkItemResponse],
)
def get_work_items(
    site_id: int,
    search: Optional[str] = None,
    status: Optional[WorkItemStatus] = None,
    priority: Optional[WorkItemPriority] = None,
    assignee_id: Optional[int] = None,
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    offset: int = Query(
        default=0,
        ge=0,
    ),
    sort_by: str = Query(
        default="created_at",
        pattern="^(created_at|due_date)$",
    ),
    sort_order: str = Query(
        default="desc",
        pattern="^(asc|desc)$",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return work_item_service.get_work_items(
        db,
        site_id,
        current_user,
        search,
        status,
        priority,
        assignee_id,
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get(
    "/work-items/{item_id}",
    response_model=WorkItemResponse,
)
def get_work_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return work_item_service.get_work_item(
        db,
        item_id,
        current_user,
    )


@router.patch(
    "/work-items/{item_id}",
    response_model=WorkItemResponse,
)
def update_work_item(
    item_id: int,
    item_data: WorkItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return work_item_service.update_work_item(
        db,
        item_id,
        item_data,
        current_user,
    )


@router.delete(
    "/work-items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_work_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    work_item_service.delete_work_item(
        db,
        item_id,
        current_user,
    )

    return None