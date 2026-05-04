# app/database/models/availability.py
from __future__ import annotations
import uuid
import enum
from datetime import datetime, time
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Time, Date, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.database.models.base import BaseModel

if TYPE_CHECKING:
    from app.database.models.user import User


class AvailabilityStatus(enum.Enum):
    available = "available"
    not_available = "not_available"


class Availability(BaseModel):
    __tablename__ = "availabilities"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    date: Mapped[datetime] = mapped_column(Date, nullable=False)

    start_time: Mapped[time] = mapped_column(Time, nullable=False)

    end_time: Mapped[time] = mapped_column(Time, nullable=False)

    status: Mapped[AvailabilityStatus] = mapped_column(
        Enum(AvailabilityStatus, name="availability_status"),
        nullable=False,
        default=AvailabilityStatus.available,
    )

    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationship back to User
    user: Mapped["User"] = relationship("User", back_populates="availabilities")

    def __repr__(self) -> str:
        return (
            f"<Availability("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"date={self.date}, "
            f"start={self.start_time}, "
            f"end={self.end_time}, "
            f"status={self.status}"
            f")>"
        )