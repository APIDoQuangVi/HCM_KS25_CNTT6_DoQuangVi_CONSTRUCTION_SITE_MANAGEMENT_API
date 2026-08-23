from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.site_member import (
    SiteMemberCreate,
    SiteMemberResponse,
)
from app.services import site_member_service


router = APIRouter(
    prefix="/construction-sites/{site_id}/members",
    tags=["Site Members"],
)


@router.post(
    "",
    response_model=SiteMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_site_member(
    site_id: int,
    member_data: SiteMemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return site_member_service.add_member(
        db,
        site_id,
        member_data,
        current_user,
    )


@router.get(
    "",
    response_model=list[SiteMemberResponse],
)
def get_site_members(
    site_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return site_member_service.get_members(
        db,
        site_id,
        current_user,
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_site_member(
    site_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    site_member_service.remove_member(
        db,
        site_id,
        user_id,
        current_user,
    )

    return None