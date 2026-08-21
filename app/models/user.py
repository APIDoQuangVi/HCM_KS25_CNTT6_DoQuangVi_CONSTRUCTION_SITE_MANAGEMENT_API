from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, Column, DateTime, Enum as SQLEnum, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash = Column(
        String(255),
        nullable=False,
    )

    full_name = Column(
        String(255),
        nullable=False,
    )

    role = Column(
        SQLEnum(UserRole),
        nullable=False,
        default=UserRole.USER,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    owned_sites = relationship(
        "ConstructionSite",
        back_populates="owner",
        foreign_keys="ConstructionSite.owner_id",
    )

    site_memberships = relationship(
        "SiteMember",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    assigned_work_items = relationship(
        "WorkItem",
        back_populates="assignee",
        foreign_keys="WorkItem.assignee_id",
    )