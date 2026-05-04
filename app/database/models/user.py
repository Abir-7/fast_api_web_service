# app/database/models/user.py
from __future__ import annotations
import enum
import uuid
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.database.models.base import BaseModel

if TYPE_CHECKING:
    from app.database.models.user_profile import UserProfile
    from app.database.models.user_authentication import UserAuthentication
    from app.database.models.actor import Actor

class UserRole(enum.Enum):
    admin = "admin"
    customer = "customer"
    cleaner = "cleaner"
    manager="manager"

class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"), 
        nullable=False, 
        server_default="customer"
    )
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    profile: Mapped[Optional[UserProfile]] = relationship(
        "UserProfile", 
        back_populates="user", 
        uselist=False,
        cascade="all, delete-orphan"
    )
    authentications: Mapped[List[UserAuthentication]] = relationship(
        "UserAuthentication",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    actor_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("actors.id", ondelete="SET NULL"), 
        unique=True, 
        nullable=True
    )
    
    actor: Mapped[Optional[Actor]] = relationship(
        "Actor",
        back_populates="user"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"