from discord.ext import commands

from app.bot import Carbon
from app.services.listeners.connections import ConnectionService


class ConnectionCog(commands.Cog):
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot
        self.service = ConnectionService(self.bot)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.service._on_ready()


async def setup(bot: Carbon):
    await bot.add_cog(ConnectionCog(bot))
