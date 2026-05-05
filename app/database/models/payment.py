# app/database/models/payment.py
from __future__ import annotations
import uuid
import enum
from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlalchemy import Enum, ForeignKey, Numeric, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database.models.base import BaseModel

if TYPE_CHECKING:
    from app.database.models.booking_request import BookingRequest


class PaymentStatus(enum.Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"
    refunded = "refunded"


class PaymentGateway(enum.Enum):
    stripe = "stripe"


class Payment(BaseModel):
    __tablename__ = "payments"

    booking_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("booking_requests.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # one payment per booking
        index=True,
    )

    # ── price breakdown (from Service Details screen) ──
    sub_total: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    service_fee: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=0.00,
    )
    tax: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=0.00,
    )
    total_amount: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    # ── gateway (stripe from payment screen) ──
    gateway: Mapped[PaymentGateway] = mapped_column(
        Enum(PaymentGateway, name="payment_gateway"),
        nullable=False,
        default=PaymentGateway.stripe,
    )
    gateway_transaction_id: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
        unique=True,
        comment="Stripe payment intent or charge ID",
    )

    # ── status ──
    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus, name="payment_status"),
        nullable=False,
        default=PaymentStatus.pending,
    )

    paid_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # ── relationship ──
    booking: Mapped["BookingRequest"] = relationship(
        "BookingRequest",
        back_populates="payment",
    )

    def __repr__(self) -> str:
        return (
            f"<Payment("
            f"id={self.id}, "
            f"booking_id={self.booking_id}, "
            f"total={self.total_amount}, "
            f"status={self.status}, "
            f"gateway={self.gateway}"
            f")>"
        )