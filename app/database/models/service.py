from __future__ import annotations
import uuid
from typing import List, TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database.models.base import BaseModel

if TYPE_CHECKING:
    from app.database.models.actor import Actor
    from app.database.models.booking_request import BookingRequest


class Service(BaseModel):
    __tablename__ = "services"

    service_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
        comment="e.g. Residential Cleaning | Deep Clean | Office Cleaning"
    )

    property_size: Mapped[str] = mapped_column(
        String,
        nullable=False,
        comment="e.g. 1 bedroom | 2 bedrooms | 3 bedrooms"
    )

    distance: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        comment="max distance in km e.g. 2 | 5 | 8"
    )

    price: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    created_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("actors.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ── relationships ──
    created_by: Mapped["Actor"] = relationship("Actor")

    booking_requests: Mapped[List["BookingRequest"]] = relationship(
        "BookingRequest",
        back_populates="service",
    )

    def __repr__(self) -> str:
        return (
            f"<Service("
            f"id={self.id}, "
            f"type={self.service_type}, "
            f"size={self.property_size}, "
            f"price={self.price}"
            f")>"
        )