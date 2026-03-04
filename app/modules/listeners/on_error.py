import discord
from discord.ext import commands

from app.bot import Carbon
from app.services.listeners.on_error import ErrorService


class ErrorCog(commands.Cog):
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot
        self.service = ErrorService(self.bot)

    @commands.Cog.listener()
    async def on_app_command_error(
        self,
        interaction: discord.Interaction,
        error: discord.app_commands.AppCommandError,
    ) -> None:
        result = await self.service._on_error(interaction, error)

        if result is not None:
            await interaction.response.send_message(embed=result, ephemeral=True)
