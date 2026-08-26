from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.site import (
    ConstructionSiteCreate,
    ConstructionSiteResponse,
    ConstructionSiteUpdate,
)
from app.services import site_service

from typing import Optional


router = APIRouter(
    prefix="/construction-sites",
    tags=["Construction Sites"],
)


@router.post(
    "",
    summary="Tạo công trình",
    description="Tạo một công trình mới cho user hiện tại.",
    response_model=ConstructionSiteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_construction_site(
    site_data: ConstructionSiteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return site_service.create_site(
        db,
        site_data,
        current_user,
    )


@router.get(
    "",
    summary="Danh sách công trình của tôi",
    description="Lấy các công trình mà user hiện tại tham gia.",
    response_model=list[ConstructionSiteResponse],
    status_code=status.HTTP_200_OK,
)
def get_my_construction_sites(
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return site_service.get_my_sites(
        db,
        current_user,
        search,
    )


@router.get(
    "/{site_id}",
    summary="Xem chi tiết công trình",
    description="Lấy thông tin công trình theo ID.",
    response_model=ConstructionSiteResponse,
    status_code=status.HTTP_200_OK,
)
def get_construction_site(
    site_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    site = site_service.get_site_by_id(
        db,
        site_id,
    )

    site_service.check_site_member(
        db,
        site_id,
        current_user.id,
    )

    return site


@router.patch(
    "/{site_id}",
    summary="Cập nhật công trình",
    description="Cập nhật thông tin công trình theo ID.",
    response_model=ConstructionSiteResponse,
    status_code=status.HTTP_200_OK,
)
def update_construction_site(
    site_id: int,
    site_data: ConstructionSiteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return site_service.update_site(
        db,
        site_id,
        site_data,
        current_user,
    )


@router.delete(
    "/{site_id}",
    summary="Xóa công trình",
    description="Xóa công trình theo ID.",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_construction_site(
    site_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    site_service.delete_site(
        db,
        site_id,
        current_user,
    )

    return None