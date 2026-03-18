import discord

from app.bot import Carbon
from app.db.services.guild_service import GuildService
from app.db.session import session_maker


class Service:
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot

    async def _guild_join(self, guild: discord.Guild) -> None:
        async with session_maker() as session, session.begin():
            await GuildService.get_or_create(session, guild.id)

    async def _guild_leave(self, guild: discord.Guild) -> None:
        async with session_maker() as session, session.begin():
            await GuildService.del_guild(session, guild.id)
