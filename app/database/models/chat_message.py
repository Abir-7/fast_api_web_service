# app/database/models/chat_message.py
from __future__ import annotations
import uuid
import enum
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import DateTime, ForeignKey, String, Text, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database.models.base import BaseModel

if TYPE_CHECKING:
    from app.database.models.chat_session import ChatSession
    from app.database.models.service import Service


class MessageRole(enum.Enum):
    user = "user"
    ai = "ai"


class MessageType(enum.Enum):
    text = "text"                   # normal message — "Hi!", "Tell me your location"
    service_suggestion = "service_suggestion"  # AI card with price + Book Now button


class ChatMessage(BaseModel):
    __tablename__ = "chat_messages"

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    role: Mapped[MessageRole] = mapped_column(
        Enum(MessageRole, name="message_role"),
        nullable=False,
        comment="user | ai"
    )

    message_type: Mapped[MessageType] = mapped_column(
        Enum(MessageType, name="message_type"),
        nullable=False,
        default=MessageType.text,
        comment="text = normal bubble | service_suggestion = card with Book Now"
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="message text or ai extra note like 'If you want to know more details...'"
    )

    # ── only set when message_type = service_suggestion ──
    service_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("services.id", ondelete="SET NULL"),
        nullable=True,
        comment="which service the AI is suggesting"
    )

    sent_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # ── relationships ──
    session: Mapped["ChatSession"] = relationship(
        "ChatSession",
        back_populates="messages",
    )
    service: Mapped[Optional["Service"]] = relationship(
        "Service",
    )

    def __repr__(self) -> str:
        return (
            f"<ChatMessage("
            f"id={self.id}, "
            f"role={self.role}, "
            f"type={self.message_type}, "
            f"session_id={self.session_id}"
            f")>"
        )