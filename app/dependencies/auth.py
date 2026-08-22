from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User

from app.core.security import decode_access_token

from app.models.user import User, UserRole


security = HTTPBearer()


def get_current_user(
    token = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Lấy user hiện tại từ JWT.
    """

    # Lấy token từ Authorization
    access_token = token.credentials

    # Giải mã token
    payload = decode_access_token(access_token)

    # Token sai hoặc hết hạn
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Token không hợp lệ hoặc đã hết hạn"
        )

    # Lấy user id từ JWT
    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Token không có user id"
        )

    # Tìm user trong database
    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User không tồn tại"
        )

    # Kiểm tra tài khoản
    if user.is_active is False:
        raise HTTPException(
            status_code=403,
            detail="Tài khoản đã bị khóa"
        )

    return user


def get_current_admin(
    current_user: User = Depends(get_current_user)
):
    """
    Chỉ cho phép ADMIN sử dụng.
    """

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Chỉ Admin mới được sử dụng chức năng này"
        )

    return current_user