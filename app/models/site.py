from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Column,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class SiteMemberRole(str, Enum):
    OWNER = "OWNER"
    MEMBER = "MEMBER"


class ConstructionSite(Base):
    __tablename__ = "construction_sites"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String(255),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    owner = relationship(
        "User",
        back_populates="owned_sites",
        foreign_keys=[owner_id],
    )

    members = relationship(
        "SiteMember",
        back_populates="site",
        cascade="all, delete-orphan",
    )

    work_items = relationship(
        "WorkItem",
        back_populates="site",
        cascade="all, delete-orphan",
    )


