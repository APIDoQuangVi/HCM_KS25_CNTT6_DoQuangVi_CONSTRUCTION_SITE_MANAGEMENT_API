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
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class WorkItemStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class WorkItemPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class WorkItem(Base):
    __tablename__ = "work_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    site_id = Column(
        Integer,
        ForeignKey("construction_sites.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title = Column(
        String(255),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    assignee_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    status = Column(
        SQLEnum(WorkItemStatus),
        nullable=False,
        default=WorkItemStatus.TODO,
    )

    priority = Column(
        SQLEnum(WorkItemPriority),
        nullable=False,
        default=WorkItemPriority.MEDIUM,
    )

    due_date = Column(
        DateTime,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    site = relationship(
        "ConstructionSite",
        back_populates="work_items",
    )

    assignee = relationship(
        "User",
        back_populates="assigned_work_items",
        foreign_keys=[assignee_id],
    )