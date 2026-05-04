# app/database/models/base.py
import uuid
from datetime import datetime
from typing import Annotated
from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

# Custom type for common primary keys
pk_uuid = Annotated[uuid.UUID, mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)]

class BaseModel(Base):
    __abstract__ = True

    id: Mapped[pk_uuid]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        onupdate=func.now(), 
        server_default=func.now()
    )