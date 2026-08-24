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
    response_model=list[ConstructionSiteResponse],
)
def get_my_construction_sites(
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return site_service.get_my_sites(
        db,
        current_user,
    )


@router.get(
    "/{site_id}",
    response_model=ConstructionSiteResponse,
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
    response_model=ConstructionSiteResponse,
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