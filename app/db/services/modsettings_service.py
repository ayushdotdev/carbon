from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.mod_settings import ModSettings
from app.db.services.guild_service import GuildService


class ModSettingsService:
    @staticmethod
    async def get_guild_config(session: AsyncSession, guild_id: int) -> ModSettings:
        result = await session.execute(
            select(ModSettings).where(ModSettings.guild_id == guild_id)
        )
        guild_config = result.scalar_one_or_none()

        if not guild_config:
            await GuildService.get_or_create(session, guild_id)
            guild_config = ModSettings(guild_id=guild_id)
            session.add(guild_config)
            try:
                await session.flush()
            except IntegrityError:
                await session.rollback()
                result = await session.execute(
                    select(ModSettings).where(ModSettings.guild_id == guild_id)
                )
                return result.scalar_one()

        return guild_config

    @staticmethod
    async def get_log_channel_id(session: AsyncSession, guild_id: int) -> int | None:
        guild_config = await ModSettingsService.get_guild_config(session, guild_id)
        return guild_config.log_channel_id

    @staticmethod
    async def set_log_channel_id(
        session: AsyncSession, guild_id: int, channel_id: int
    ) -> None:
        guild_config = await ModSettingsService.get_guild_config(session, guild_id)
        guild_config.log_channel_id = channel_id

        try:
            await session.flush()
        except IntegrityError:
            await session.rollback()

    @staticmethod
    async def is_mod_dm_enabled(session: AsyncSession, guild_id: int) -> bool:
        guild_config = await ModSettingsService.get_guild_config(session, guild_id)
        return guild_config.is_dm_enabled
