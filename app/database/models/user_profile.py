# app/database/models/user_profile.py
from __future__ import annotations
import uuid
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.database.models.base import BaseModel

if TYPE_CHECKING:
    from app.database.models.user import User

class UserProfile(BaseModel):
    __tablename__ = "user_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        unique=True, 
        nullable=False
    )
    full_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    user: Mapped[User] = relationship("User", back_populates="profile")

    def __repr__(self) -> str:
        return f"<UserProfile(id={self.id}, user_id={self.user_id}, full_name={self.full_name})>"