from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.site import ConstructionSite
from app.models.site_member import SiteMember
from app.models.user import User
from app.models.work_item import WorkItem
from app.schemas.work_item import (
    WorkItemCreate,
    WorkItemUpdate,
)


def check_member(
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


def create_work_item(
    db: Session,
    site_id: int,
    item_data: WorkItemCreate,
    current_user: User,
):
    check_member(
        db,
        site_id,
        current_user.id,
    )

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

    if item_data.assignee_id is not None:
        assignee = (
            db.query(SiteMember)
            .filter(
                SiteMember.site_id == site_id,
                SiteMember.user_id == item_data.assignee_id,
            )
            .first()
        )

        if not assignee:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assignee phải là thành viên của công trình",
            )

    work_item = WorkItem(
        site_id=site_id,
        title=item_data.title,
        description=item_data.description,
        assignee_id=item_data.assignee_id,
        status=item_data.status,
        priority=item_data.priority,
        due_date=item_data.due_date,
    )

    db.add(work_item)
    db.commit()
    db.refresh(work_item)

    return work_item


def get_work_items(
    db: Session,
    site_id: int,
    current_user: User,
):
    check_member(
        db,
        site_id,
        current_user.id,
    )

    return (
        db.query(WorkItem)
        .filter(WorkItem.site_id == site_id)
        .all()
    )


def get_work_item(
    db: Session,
    item_id: int,
    current_user: User,
):
    item = (
        db.query(WorkItem)
        .filter(WorkItem.id == item_id)
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hạng mục thi công không tồn tại",
        )

    check_member(
        db,
        item.site_id,
        current_user.id,
    )

    return item


def update_work_item(
    db: Session,
    item_id: int,
    item_data: WorkItemUpdate,
    current_user: User,
):
    item = get_work_item(
        db,
        item_id,
        current_user,
    )

    member = check_member(
        db,
        item.site_id,
        current_user.id,
    )

    if (
        member.role != "OWNER"
        and item.assignee_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có permission cập nhật hạng mục này",
        )

    update_data = item_data.model_dump(
        exclude_unset=True
    )

    if "assignee_id" in update_data:
        if update_data["assignee_id"] is not None:
            assignee = (
                db.query(SiteMember)
                .filter(
                    SiteMember.site_id == item.site_id,
                    SiteMember.user_id
                    == update_data["assignee_id"],
                )
                .first()
            )

            if not assignee:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Assignee phải là thành viên của công trình",
                )

    for key, value in update_data.items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)

    return item


def delete_work_item(
    db: Session,
    item_id: int,
    current_user: User,
):
    item = get_work_item(
        db,
        item_id,
        current_user,
    )

    member = check_member(
        db,
        item.site_id,
        current_user.id,
    )

    if (
        member.role != "OWNER"
        and item.assignee_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có permission xóa hạng mục này",
        )

    db.delete(item)
    db.commit()