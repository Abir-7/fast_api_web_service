from __future__ import annotations
import uuid
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database.models.base import BaseModel

if TYPE_CHECKING:
    from app.database.models.actor import Actor

class Guest(BaseModel):
    __tablename__ = "guests"

    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    actor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("actors.id", ondelete="CASCADE"), 
        unique=True, 
        nullable=False
    )

    actor: Mapped[Actor] = relationship("Actor", back_populates="guest")

    def __repr__(self) -> str:
        return f"<Guest(id={self.id}, name={self.name})>"
