from datetime import datetime
from typing import Self

from sqlalchemy import TIMESTAMP, BigInteger, Boolean, ForeignKey, select
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.db.models.guild import Guild


class ModSettings(Base):
    __tablename__ = "mod_settings"

    guild_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("guild.id", ondelete="CASCADE"), primary_key=True
    )
    is_dm_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    log_channel_id: Mapped[int | None] = mapped_column(BigInteger)
    reason_aliases: Mapped[list[dict]] = mapped_column(
        JSONB, nullable=False, default=list
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    guild = relationship("Guild", back_populates="mod_settings")

    @classmethod
    async def get_guild_mod_conf(cls, session: AsyncSession, guild_id: int) -> Self:
        result = await session.execute(select(cls).where(cls.guild_id == guild_id))
        guild_conf = result.scalar_one_or_none()
        if not guild_conf:
            guild = await Guild.get_or_create(session, guild_id)
            return guild.mod_settings

        return guild_conf

    @classmethod
    async def get_log_channel_id(
        cls, session: AsyncSession, guild_id: int
    ) -> int | None:
        result = await session.execute(
            select(cls.log_channel_id).where(cls.guild_id == guild_id)
        )
        return result.scalar_one_or_none()

    @classmethod
    async def set_log_channel_id(
        cls, session: AsyncSession, guild_id: int, log_channel_id: int
    ) -> None:
        result = await session.execute(select(cls).where(cls.guild_id == guild_id))
        guild_settings = result.scalar_one_or_none()

        if guild_settings is None:
            return

        guild_settings.log_channel_id = log_channel_id
        await session.flush()

    @classmethod
    async def get_if_dm_enabled(
        cls, session: AsyncSession, guild_id: int
    ) -> bool | None:
        result = await session.execute(
            select(cls.is_dm_enabled).where(cls.guild_id == guild_id)
        )
        return result.scalar_one_or_none()
