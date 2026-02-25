from typing import Optional
from datetime import datetime
from sqlalchemy import (
    TIMESTAMP,
    BigInteger,
    CheckConstraint,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.base import Base
from app.helpers.enums import ActionType


class CaseLog(Base):
    __tablename__ = "case_logs"

    case_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    guild_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("guilds.id", ondelete="CASCADE")
    )
    target_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    moderator_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    action_type: Mapped[ActionType] = mapped_column(Enum(ActionType), nullable=False)
    reason: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    updated_by: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    duration: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )

    __table_args__ = (
        Index("ix_case_logs_guild_id", "guild_id"),
        Index("ix_case_logs_target_id", "target_id"),
        Index("ix_case_logs_mod_id", "moderator_id"),
        CheckConstraint(
            "duration is NULL or duration >= 0", name="cx_duration_seconds_is_positive"
        ),
    )
