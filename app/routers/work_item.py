from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return work_item_service.get_work_items(
        db,
        site_id,
        current_user,
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