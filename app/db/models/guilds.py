from typing import Optional
from sqlalchemy import TIMESTAMP, BigInteger, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.base import Base
from datetime import datetime


class Guilds(Base):
    __tablename__ = "guilds"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    prefix: Mapped[str] = mapped_column(String, default="!", nullable=False)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    premium_expires_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True))
    language: Mapped[str] = mapped_column(String(5), default="en", nullable=False)
    joined_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    mod_settings = relationship(
        "ModSettings",
        back_populates="guilds",
        cascade="all, delete-orphan",
        uselist=False,
    )
    appeal_settings = relationship(
        "AppealSettings",
        back_populates="guilds",
        cascade="all, delete-orphan",
        uselist=False,
    )
