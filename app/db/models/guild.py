from datetime import datetime

from sqlalchemy import TIMESTAMP, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Guild(Base):
    __tablename__ = "guild"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    premium_expires_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True)
    )
    joined_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    mod_settings = relationship(
        "ModSettings",
        back_populates="guild",
        cascade="all, delete-orphan",
        uselist=False,
    )
    appeal_settings = relationship(
        "AppealSettings",
        back_populates="guild",
        cascade="all, delete-orphan",
        uselist=False,
    )
