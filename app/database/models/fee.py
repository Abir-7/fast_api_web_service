from __future__ import annotations
from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.database.models.base import BaseModel

class Fee(BaseModel):
    __tablename__ = "fees"

    tax_fee: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0.00)
    service_fee: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0.00)

    def __repr__(self) -> str:
        return f"<Fee(id={self.id}, tax_fee={self.tax_fee}, service_fee={self.service_fee})>"
