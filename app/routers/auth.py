from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.user import User, UserRole

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse
)

from app.schemas.user import UserResponse

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    summary="Đăng ký tài khoản",
    description="Tạo tài khoản người dùng mới.",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):

    # Tìm email trong database
    old_user = db.query(User).filter(
        User.email == data.email
    ).first()

    # Email đã tồn tại
    if old_user:
        raise HTTPException(
            status_code=400,
            detail="Email đã tồn tại"
        )

    # Hash password
    password_hash = hash_password(
        data.password
    )

    # Tạo user
    user = User(
        email=data.email,
        password_hash=password_hash,
        full_name=data.full_name,
        role=UserRole.USER,
        is_active=True
    )

    # Lưu database
    db.add(user)

    db.commit()

    db.refresh(user)

    return user


@router.post(
    "/login",
    summary="Đăng nhập",
    description="Xác thực tài khoản và cấp JWT access token.",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    # Tìm user
    user = db.query(User).filter(
        User.email == data.email
    ).first()

    # Không tìm thấy user
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Email hoặc password không đúng"
        )

    # Kiểm tra password
    password_correct = verify_password(
        data.password,
        user.password_hash
    )

    if password_correct is False:
        raise HTTPException(
            status_code=401,
            detail="Email hoặc password không đúng"
        )

    # Kiểm tra tài khoản
    if user.is_active is False:
        raise HTTPException(
            status_code=403,
            detail="Tài khoản đã bị khóa"
        )

    # Tạo JWT
    token_data = {
        "sub": str(user.id)
    }

    access_token = create_access_token(
        token_data
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }