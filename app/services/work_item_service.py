from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.site import ConstructionSite
from app.models.site_member import SiteMember
from app.models.user import User
from app.models.work_item import (
    WorkItem,
    WorkItemPriority,
    WorkItemStatus,
)
from app.schemas.work_item import (
    WorkItemCreate,
    WorkItemUpdate,
)

from typing import Optional

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

    check_member(
        db,
        site_id,
        current_user.id,
    )
    if item_data.assignee_id == 0 :
        item_data.assignee_id = current_user.id 
    elif item_data.assignee_id is not None:
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
    search: Optional[str] = None,
    item_status: Optional[WorkItemStatus] = None,
    priority: Optional[WorkItemPriority] = None,
    assignee_id: Optional[int] = None,
    limit: int = 20,
    offset: int = 0,
    sort_by: str = "created_at",
    sort_order: str = "desc",
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

    check_member(
        db,
        site_id,
        current_user.id,
    )

    query = (
        db.query(WorkItem)
        .filter(WorkItem.site_id == site_id)
    )

    if search:
        search = search.strip()

    if search:
        query = query.filter(
            WorkItem.title.ilike(f"%{search}%")
        )

    if item_status is not None:
        query = query.filter(
            WorkItem.status == item_status
        )

    if priority is not None:
        query = query.filter(
            WorkItem.priority == priority
        )
    if assignee_id is not None:
        query = query.filter(
            WorkItem.assignee_id == assignee_id
        )
    sort_column = {
        "created_at": WorkItem.created_at,
        "due_date": WorkItem.due_date,
    }[sort_by]

    if sort_order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    return (
    query
    
    .offset(offset)
    .limit(limit)
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

    member = (
    db.query(SiteMember)
    .filter(
        SiteMember.site_id == item.site_id,
        SiteMember.user_id == current_user.id,
    )
    .first()
)

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không phải thành viên của công trình",
        )

    is_owner = member.role == "OWNER"
    is_assignee = item.assignee_id == current_user.id

    if not is_owner and not is_assignee:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền cập nhật hạng mục này",
        )

    update_data = item_data.model_dump(
        exclude_unset=True
    )
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không có dữ liệu để cập nhật",
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
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Không thể giao việc cho người ngoài công trình",
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

    member = (
    db.query(SiteMember)
    .filter(
        SiteMember.site_id == item.site_id,
        SiteMember.user_id == current_user.id,
    )
    .first()
)

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không phải thành viên của công trình",
        )

    is_owner = member.role == "OWNER"
    is_assignee = item.assignee_id == current_user.id

    if not is_owner and not is_assignee:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền xóa hạng mục này",
        )

    db.delete(item)
    db.commit()