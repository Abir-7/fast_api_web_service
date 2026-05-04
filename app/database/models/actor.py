from __future__ import annotations
import enum
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.models.base import BaseModel
from app.database.models.booking_request import BookingRequest

if TYPE_CHECKING:
    from app.database.models.user import User
    from app.database.models.guest import Guest

class ActorType(enum.Enum):
    customer = "customer"
    guest = "guest"

class Actor(BaseModel):
    __tablename__ = "actors"

    type: Mapped[ActorType] = mapped_column(
        Enum(ActorType, name="actor_type"), 
        nullable=False,
        server_default="guest"
    )

    user: Mapped[Optional[User]] = relationship("User", back_populates="actor", uselist=False)
    guest: Mapped[Optional[Guest]] = relationship("Guest", back_populates="actor", uselist=False)

    booking_requests: Mapped[List["BookingRequest"]] = relationship(
    "BookingRequest", back_populates="actor"
)

    def __repr__(self) -> str:
        return f"<Actor(id={self.id}, type={self.type})>"
