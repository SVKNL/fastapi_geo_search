from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.association import organization_activities

if TYPE_CHECKING:
    from app.models.organization import Organization


class Activity(Base):
    __tablename__ = "activities"
    __table_args__ = (
        UniqueConstraint("parent_id", "name", name="uq_activities_parent_name"),
        CheckConstraint(
            "depth >= 1 AND depth <= 3", name="ck_activity_depth_range"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("activities.id", ondelete="CASCADE"), nullable=True
    )
    depth: Mapped[int] = mapped_column(Integer)

    parent: Mapped[Activity | None] = relationship(
        "Activity", remote_side="Activity.id", back_populates="children"
    )
    children: Mapped[list[Activity]] = relationship(
        "Activity", back_populates="parent", cascade="all, delete-orphan"
    )
    organizations: Mapped[list[Organization]] = relationship(
        "Organization",
        secondary=organization_activities,
        back_populates="activities",
    )
