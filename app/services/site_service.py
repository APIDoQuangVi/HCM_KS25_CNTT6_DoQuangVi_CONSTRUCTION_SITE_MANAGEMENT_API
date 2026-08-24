from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.site import ConstructionSite
from app.models.site_member import SiteMember, SiteMemberRole
from app.models.user import User
from app.schemas.site import (
    ConstructionSiteCreate,
    ConstructionSiteUpdate,
)

from typing import Optional


def create_site(
    db: Session,
    site_data: ConstructionSiteCreate,
    current_user: User,
):
    site = ConstructionSite(
        name=site_data.name,
        description=site_data.description,
        owner_id=current_user.id,
    )

    db.add(site)
    db.commit()
    db.refresh(site)

    owner_member = SiteMember(
        site_id=site.id,
        user_id=current_user.id,
        role=SiteMemberRole.OWNER,
    )

    db.add(owner_member)
    db.commit()

    return site


def get_my_sites(
    db: Session,
    current_user: User,
    search: Optional[str] = None,
):
    query = (
        db.query(ConstructionSite)
        .join(
            SiteMember,
            SiteMember.site_id == ConstructionSite.id,
        )
        .filter(
            SiteMember.user_id == current_user.id
        )
    )

    if search:
        search = search.strip()

        if search:
            query = query.filter(
                ConstructionSite.name.ilike(f"%{search}%")
            )

    return query.all()


def get_site_by_id(
    db: Session,
    site_id: int,
):
    site = (
        db.query(ConstructionSite)
        .filter(ConstructionSite.id == site_id)
        .first()
    )

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Công trình không tồn tại",
        )

    return site


def check_site_member(
    db: Session,
    site_id: int,
    user_id: int,
):
    member = (
        db.query(SiteMember)
        .filter(
            SiteMember.site_id == site_id,
            SiteMember.user_id == user_id,
        )
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không phải thành viên của công trình",
        )

    return member


def check_site_owner(
    db: Session,
    site_id: int,
    user_id: int,
):
    site = get_site_by_id(db, site_id)

    if site.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ Owner mới được thực hiện thao tác này",
        )

    return site


def update_site(
    db: Session,
    site_id: int,
    site_data: ConstructionSiteUpdate,
    current_user: User,
):
    site = check_site_owner(
        db,
        site_id,
        current_user.id,
    )

    if site_data.name is not None:
        site.name = site_data.name

    if site_data.description is not None:
        site.description = site_data.description

    db.commit()
    db.refresh(site)

    return site


def delete_site(
    db: Session,
    site_id: int,
    current_user: User,
):
    site = check_site_owner(
        db,
        site_id,
        current_user.id,
    )

    db.delete(site)
    db.commit()

    return None