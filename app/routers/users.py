from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.user import User

from app.schemas.user import UserResponse

from app.dependencies.auth import (
    get_current_user,
    get_current_admin
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/me",
    response_model=UserResponse
)
def get_my_profile(
    current_user: User = Depends(
        get_current_user
    )
):

    return current_user


@router.get(
    "",
    response_model=list[UserResponse]
)
def get_all_users(
    search: str | None = None,
    is_active: bool | None = None,

    current_admin: User = Depends(
        get_current_admin
    ),

    db: Session = Depends(get_db)
):

    query = db.query(User)

    # Search tên hoặc email
    if search:

        query = query.filter(
            (User.full_name.ilike(
                f"%{search}%"
            ))
            |
            (User.email.ilike(
                f"%{search}%"
            ))
        )

    # Filter trạng thái
    if is_active is not None:

        query = query.filter(
            User.is_active == is_active
        )

    users = query.all()

    return users