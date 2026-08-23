from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.site import ConstructionSite
from app.models.site_member import SiteMember, SiteMemberRole
from app.models.user import User
from app.schemas.site_member import SiteMemberCreate


def add_member(
    db: Session,
    site_id: int,
    member_data: SiteMemberCreate,
    current_user: User,
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

    if site.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ Owner mới được thêm thành viên",
        )

    user = (
        db.query(User)
        .filter(User.id == member_data.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User không tồn tại",
        )

    existing_member = (
        db.query(SiteMember)
        .filter(
            SiteMember.site_id == site_id,
            SiteMember.user_id == member_data.user_id,
        )
        .first()
    )

    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User đã là thành viên của công trình",
        )

    if member_data.role == SiteMemberRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không thể thêm thành viên với role OWNER",
        )

    member = SiteMember(
        site_id=site_id,
        user_id=member_data.user_id,
        role=SiteMemberRole.MEMBER,
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    return member


def get_members(
    db: Session,
    site_id: int,
    current_user: User,
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

    member = (
        db.query(SiteMember)
        .filter(
            SiteMember.site_id == site_id,
            SiteMember.user_id == current_user.id,
        )
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không phải thành viên của công trình",
        )

    return (
        db.query(SiteMember)
        .filter(SiteMember.site_id == site_id)
        .all()
    )


def remove_member(
    db: Session,
    site_id: int,
    user_id: int,
    current_user: User,
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

    if site.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ Owner mới được xóa thành viên",
        )

    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Owner không thể tự xóa chính mình",
        )

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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thành viên không tồn tại trong công trình",
        )

    db.delete(member)
    db.commit()