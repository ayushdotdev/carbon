import pendulum
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.guild import Guild


class GuildService:
    @staticmethod
    async def get_or_create(session: AsyncSession, guild_id: int) -> Guild:
        result = await session.execute(select(Guild).where(Guild.id == guild_id))
        guild = result.scalar_one_or_none()

        if guild:
            return guild

        guild = Guild(id=guild_id, joined_at=pendulum.now("UTC"))
        session.add(guild)

        try:
            await session.flush()
        except IntegrityError:
            await session.rollback()
            result = await session.execute(select(Guild).where(Guild.id == guild_id))
            return result.scalar_one()

        return guild

    @staticmethod
    async def del_guild(session: AsyncSession, guild_id: int) -> None:
        result = await session.execute(select(Guild).where(Guild.id == guild_id))
        guild = result.scalar_one()

        if guild.is_premium:
            return

        await session.delete(guild)

        try:
            await session.flush()
        except IntegrityError:
            await session.rollback()
