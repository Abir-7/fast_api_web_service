# app/database/models/chat_session.py
from __future__ import annotations
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database.models.base import BaseModel

if TYPE_CHECKING:
    from app.database.models.actor import Actor
    from app.database.models.chat_message import ChatMessage


class ChatSession(BaseModel):
    __tablename__ = "chat_sessions"

    actor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("actors.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,        # ONE session per actor forever
        index=True,
    )

    # ── relationships ──
    actor: Mapped["Actor"] = relationship(
        "Actor",
        back_populates="chat_session",
    )
    messages: Mapped[list["ChatMessage"]] = relationship(
        "ChatMessage",
        back_populates="session",
        order_by="ChatMessage.sent_at",
        cascade="all, delete-orphan",
    )