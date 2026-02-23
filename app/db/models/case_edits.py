from datetime import datetime
from typing import Optional
from sqlalchemy import TIMESTAMP, BigInteger, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.base import Base


class CaseEdit(Base):
    __tablename__ = "case_edits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    case_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("case_logs.case_id", ondelete="CASCADE")
    )
    old_reason: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    new_reason: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    edited_by: Mapped[int] = mapped_column(BigInteger, nullable=False)
    edited_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now()
    )

    __table_args__ = (
        Index("ix_case_edits_case_id", "case_id"),
        Index("ix_case_edits_mod_id", "edited_by"),
    )
