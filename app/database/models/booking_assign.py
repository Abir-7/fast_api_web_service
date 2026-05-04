# app/database/models/booking_assign.py
from __future__ import annotations
import uuid
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database.models.base import BaseModel

if TYPE_CHECKING:
    from app.database.models.user import User
    from app.database.models.booking_request import BookingRequest


class BookingAssign(BaseModel):
    __tablename__ = "booking_assigns"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    booking_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("booking_requests.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # one assign per booking
    )

    user: Mapped["User"] = relationship("User", back_populates="booking_assigns")
    booking: Mapped["BookingRequest"] = relationship("BookingRequest", back_populates="booking_assign")

    def __repr__(self) -> str:
        return (
            f"<BookingAssign("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"booking_id={self.booking_id}"
            f")>"
        )