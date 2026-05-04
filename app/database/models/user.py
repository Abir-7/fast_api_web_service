# app/database/models/user.py
from __future__ import annotations
import enum
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Boolean, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.models.base import BaseModel

if TYPE_CHECKING:
    from app.database.models.user_profile import UserProfile
    from app.database.models.user_authentication import UserAuthentication

class UserRole(enum.Enum):
    admin = "admin"
    customer = "customer"
    mechanic = "mechanic"

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

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"