# app/database/models/booking_request.py
from __future__ import annotations
import uuid
import enum
from typing import TYPE_CHECKING, Optional
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database.models.base import BaseModel
from app.database.models.booking_assign import BookingAssign

if TYPE_CHECKING:
    from app.database.models.actor import Actor
    from app.database.models.service import Service


class BookingStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    running = "running"
    completed = "completed"


class BookingRequest(BaseModel):
    __tablename__ = "booking_requests"

    service_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("services.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    actor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("actors.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    status: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus, name="booking_status"),
        nullable=False,
        default=BookingStatus.pending,
    )

    actor: Mapped["Actor"] = relationship("Actor", back_populates="booking_requests")
    service: Mapped["Service"] = relationship("Service", back_populates="booking_requests")
    booking_assign: Mapped[Optional["BookingAssign"]] = relationship(
    "BookingAssign", back_populates="booking", uselist=False
)
    def __repr__(self) -> str:
        return (
            f"<BookingRequest("
            f"id={self.id}, "
            f"service_id={self.service_id}, "
            f"actor_id={self.actor_id}, "
            f"status={self.status}"
            f")>"
        )