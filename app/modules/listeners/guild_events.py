import discord
from discord.ext import commands

from app.bot import Carbon
from app.services.listeners.guild_events import Service


class GuildEventCog(commands.Cog):
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot
        self.service = Service(self.bot)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        await self.service._guild_join(guild)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        await self.service._guild_leave(guild)


async def setup(bot: Carbon):
    await bot.add_cog(GuildEventCog(bot))
