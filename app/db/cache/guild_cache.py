from sqlalchemy.ext.asyncio import AsyncSession

from app.bot import Carbon
from app.db.services.modsettings_service import ModSettingsService


class GuildCache:
    def __init__(self) -> None:
        pass

    @staticmethod
    async def get_modlog_channel_id(
        bot: Carbon, session: AsyncSession, guild_id: int
    ) -> int | None:
        key = f"carbon:guild:{guild_id}:modlog_channel_id"
        cached = await bot.redis.get(key)

        if cached is not None:
            return int(cached)

        channel_id = await ModSettingsService.get_log_channel_id(session, guild_id)

        if channel_id is not None:
            await bot.redis.set(key, channel_id, 3600)

        return channel_id

    @staticmethod
    async def get_if_dm_enabled(
        bot: Carbon, session: AsyncSession, guild_id: int
    ) -> bool | None:
        key = f"carbon:guild:{guild_id}:is_dm_enabled"
        cache = await bot.redis.get(key)

        if cache is not None:
            return cache == 1

        is_dm_enabled = await ModSettingsService.is_mod_dm_enabled(session, guild_id)

        if is_dm_enabled is not None:
            await bot.redis.set(key, 1 if is_dm_enabled else 0, 3600)

        return is_dm_enabled
