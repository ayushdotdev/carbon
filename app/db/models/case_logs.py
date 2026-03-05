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
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base
from app.utils.confs.enums import ActionType


class CaseLog(Base):
    __tablename__ = "case_logs"

    case_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("guild.id", ondelete="CASCADE")
    )
    target_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    moderator_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    action_type: Mapped[ActionType] = mapped_column(Enum(ActionType), nullable=False)
    reason: Mapped[str | None] = mapped_column(String, nullable=True)
    updated_by: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    duration: Mapped[int | None] = mapped_column(Integer, nullable=True)
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

    @classmethod
    async def add_log(
        cls,
        session: AsyncSession,
        guild_id: int,
        target_id: int,
        moderator_id: int,
        action_type: ActionType,
        reason: str,
        duration: int = 0,
    ) -> int:
        case_log = cls(
            guild_id=guild_id,
            target_id=target_id,
            moderator_id=moderator_id,
            action_type=action_type,
            reason=reason,
            duration=duration,
        )
        session.add(case_log)
        await session.flush()
        return case_log.case_id
