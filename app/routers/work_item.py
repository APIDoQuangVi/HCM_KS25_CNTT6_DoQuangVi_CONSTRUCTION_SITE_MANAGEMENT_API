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
    WorkItemPaginatedResponse,
    WorkItemResponse,
    WorkItemUpdate,
)
from app.services import work_item_service


router = APIRouter(
    tags=["Work Items"],
)


@router.post(
    "/construction-sites/{site_id}/work-items",
    summary="Tạo hạng mục thi công",
    description="Tạo hạng mục mới. Nếu không truyền assignee_id, hạng mục được giao cho user hiện tại.",
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
    summary="Danh sách hạng mục thi công",
    description="Lấy danh sách hạng mục với bộ lọc, phân trang và sắp xếp.",
    response_model=WorkItemPaginatedResponse,
    status_code=status.HTTP_200_OK,
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
    summary="Xem hạng mục thi công",
    description="Lấy thông tin chi tiết của một hạng mục thi công.",
    response_model=WorkItemResponse,
    status_code=status.HTTP_200_OK,
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
    summary="Cập nhật hạng mục thi công",
    description="Cập nhật một phần thông tin của hạng mục thi công.",
    response_model=WorkItemResponse,
    status_code=status.HTTP_200_OK,
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
    summary="Xóa hạng mục thi công",
    description="Xóa một hạng mục thi công theo ID.",
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