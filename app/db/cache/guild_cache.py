from sqlalchemy.ext.asyncio import AsyncSession
from app.bot import Carbon
from app.db.models.mod_settings import ModSettings


class GuildCache:
    def __init__(self) -> None:
        pass

    @classmethod
    async def get_modlog_channel_id(
        cls, bot: Carbon, session: AsyncSession, guild_id: int
    ) -> int | None:
        key = f"carbon:guild:{guild_id}:modlog_channel_id"
        cached = await bot.redis.get(key)

        if cached is not None:
            return cached

        channel_id = await ModSettings.get_log_channel_id(session, guild_id)

        if channel_id is not None:
            await bot.redis.set(key, channel_id, 3600)

        return channel_id
