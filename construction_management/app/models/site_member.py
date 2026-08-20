from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class SiteMemberRole(str, Enum):
    OWNER = "OWNER"
    MEMBER = "MEMBER"


class SiteMember(Base):
    __tablename__ = "site_members"
    __table_args__ = (
        UniqueConstraint("site_id", "user_id", name="uq_site_member"),
    )

    site_id: Mapped[int] = mapped_column(
        ForeignKey("construction_sites.id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    role: Mapped[SiteMemberRole] = mapped_column(
        SQLEnum(SiteMemberRole),
        nullable=False,
    )
    joined_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    site = relationship("ConstructionSite", back_populates="members")
    user = relationship("User", back_populates="site_memberships")
