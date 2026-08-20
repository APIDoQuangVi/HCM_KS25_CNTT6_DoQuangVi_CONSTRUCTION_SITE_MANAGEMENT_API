from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class ConstructionSite(Base):
    __tablename__ = "construction_sites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

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
