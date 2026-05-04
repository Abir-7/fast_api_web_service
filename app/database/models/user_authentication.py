# app/database/models/user_authentication.py
from __future__ import annotations
import uuid
import enum
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, ForeignKey, DateTime, Enum, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.models.base import BaseModel

if TYPE_CHECKING:
    from app.database.models.user import User

class AuthStatus(enum.Enum):
    pending = "pending"
    success = "success"
    expire = "expire"

class UserAuthentication(BaseModel):
    __tablename__ = "user_authentications"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False
    )
    code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    expire_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[AuthStatus] = mapped_column(
        Enum(AuthStatus, name="auth_status"), 
        nullable=False, 
        server_default="pending"
    )

    # Relationship
    user: Mapped[User] = relationship("User", back_populates="authentications")
    
    def __repr__(self) -> str:
        return f"<UserAuthentication(id={self.id}, user_id={self.user_id}, status={self.status})>"

Index("idx_user_auth_user_created", UserAuthentication.user_id, UserAuthentication.created_at)