# app/database/models/faq.py
from __future__ import annotations
from sqlalchemy import String, Text, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database.models.base import BaseModel


class FAQ(BaseModel):
    __tablename__ = "faqs"

    question: Mapped[str] = mapped_column(String(500), nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return (
            f"<FAQ("
            f"id={self.id}, "
            f"question={self.question[:50]}, "
            f"is_active={self.is_active}"
            f")>"
        )