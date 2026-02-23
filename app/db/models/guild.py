from typing import Optional
from sqlalchemy import TIMESTAMP, BigInteger, Boolean, String
from sqlalchemy.orm  import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.base import Base
from datetime import datetime


class Guild(Base):
    __tablename__ = "guilds"

    guild_id : Mapped[int] = mapped_column(BigInteger, primary_key=True)
    prefix : Mapped[str] = mapped_column(String, default='!', nullable=False)
    is_premium : Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    premium_expires_at : Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True))
    joined_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(),onupdate=func.now(), nullable=False)

