from datetime import datetime

import pendulum
from sqlalchemy import TIMESTAMP, BigInteger, Boolean, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.db.models.appeal_settings import AppealSettings
from app.db.models.mod_settings import ModSettings


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

    @classmethod
    async def get_or_create(cls, session: AsyncSession, guild_id: int) -> "Guild":
        result = await session.execute(select(cls).where(cls.id == guild_id))
        guild = result.scalar_one_or_none()

        if guild:
            return guild

        guild = cls(id=guild_id, joined_at=pendulum.now("UTC"))

        session.add(guild)

        try:
            await session.flush()
        except IntegrityError:
            await session.rollback()
            result = await session.execute(select(cls).where(cls.id == guild_id))
            guild = result.scalar_one()
            return guild

        result = await session.execute(
            select(ModSettings).where(ModSettings.guild_id == guild.id)
        )
        mod = result.scalar_one_or_none()

        if mod is None:
            session.add(ModSettings(guild_id=guild.id))

        result = await session.execute(
            select(AppealSettings).where(ModSettings.guild_id == guild.id)
        )
        apl = result.scalar_one_or_none()

        if apl is None:
            session.add(AppealSettings(guild_id=guild.id))

        await session.flush()
        return guild
