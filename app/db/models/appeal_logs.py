from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy import TIMESTAMP, BigInteger, Enum, ForeignKey, Index, Integer, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.helpers.enums import AppealStatus


class AppealLog(Base):
    __tablename__ = "appeal_logs"

    appeal_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    guild_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("guilds.id", ondelete="CASCADE")
    )
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    case_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("case_logs.case_id", ondelete="CASCADE")
    )
    status: Mapped[AppealStatus] = mapped_column(Enum(AppealStatus), nullable=False)
    responses: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    reviewed_by: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )

    __table_args__ = Index("ix_appeal_logs_guild_id", "guild_id")
