from fastapi import APIRouter, Depends, HTTPException
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
    response_model=UserResponse,
    status_code=201
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):

    # =========================
    # 1. Kiểm tra email
    # =========================

    old_user = db.query(User).filter(
        User.email == data.email
    ).first()

    if old_user:
        raise HTTPException(
            status_code=400,
            detail="Email đã tồn tại"
        )

    # =========================
    # 2. Hash password
    # =========================

    password_hash = hash_password(
        data.password
    )

    # =========================
    # 3. Tạo user
    # =========================

    user = User(
        email=data.email,
        password_hash=password_hash,
        full_name=data.full_name,
        role=UserRole.USER,
        is_active=True
    )

    # =========================
    # 4. Lưu database
    # =========================

    db.add(user)

    db.commit()

    db.refresh(user)

    return user


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    # =========================
    # 1. Tìm user
    # =========================

    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Email hoặc password không đúng"
        )

    # =========================
    # 2. Kiểm tra password
    # =========================

    password_correct = verify_password(
        data.password,
        user.password_hash
    )

    if password_correct is False:
        raise HTTPException(
            status_code=401,
            detail="Email hoặc password không đúng"
        )

    # =========================
    # 3. Kiểm tra tài khoản
    # =========================

    if user.is_active is False:
        raise HTTPException(
            status_code=403,
            detail="Tài khoản đã bị khóa"
        )

    # =========================
    # 4. Tạo JWT
    # =========================

    token_data = {
        "sub": str(user.id)
    }

    access_token = create_access_token(
        token_data
    )

    # =========================
    # 5. Trả token
    # =========================

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }