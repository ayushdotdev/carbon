import discord
from discord.ext import commands

from app.bot import Carbon


class ErrorCog(commands.Cog):
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_app_command_error(
        self,
        interaction: discord.Interaction,
        error: discord.app_commands.AppCommandError,
    ) -> None:
        pass
