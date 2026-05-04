from __future__ import annotations
import enum
import uuid
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, Enum, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database.models.base import BaseModel
from app.database.models.booking_request import BookingRequest

if TYPE_CHECKING:
    from app.database.models.actor import Actor

class ServiceType(enum.Enum):
    plumbing = "plumbing"
    electrical = "electrical"
    cleaning = "cleaning"
    repair = "repair"
    other = "other"

class PropertyType(enum.Enum):
    residential = "residential"
    commercial = "commercial"
    industrial = "industrial"

class Service(BaseModel):
    __tablename__ = "services"

    service_type: Mapped[ServiceType] = mapped_column(
        Enum(ServiceType, name="service_type"), 
        nullable=False
    )
    property_type: Mapped[PropertyType] = mapped_column(
        Enum(PropertyType, name="property_type"), 
        nullable=False
    )
    distance: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    
    created_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("actors.id", ondelete="CASCADE"), 
        nullable=False
    )

    created_by: Mapped[Actor] = relationship("Actor")

    booking_requests: Mapped[List["BookingRequest"]] = relationship(
    "BookingRequest", back_populates="service"
)

    def __repr__(self) -> str:
        return f"<Service(id={self.id}, type={self.service_type}, price={self.price})>"
