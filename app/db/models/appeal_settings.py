from datetime import datetime
from typing import Optional
from sqlalchemy import (
    TIMESTAMP,
    BigInteger,
    Boolean,
    CheckConstraint,
    ForeignKey,
    Integer,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.base import Base


class AppealSettings(Base):
    __tablename__ = "appeal_settings"

    guild_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("guilds.id", ondelete="CASCADE"), primary_key=True
    )
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    log_channel_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    questions: Mapped[list[dict]] = mapped_column(JSONB, nullable=False, default=list)
    schema_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    guilds = relationship("Guilds", back_populates="appeal_settings")

    __table_args__ = CheckConstraint(
        "schema_version > 0", name="ck_appeal_schema_version"
    )
