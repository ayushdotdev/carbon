import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import locale_str
from app.services.commands.general import GeneralService


class General(commands.Cog):
    def __init__(self, bot: discord.Client) -> None:
        self.bot = bot
        self.service = GeneralService

    @app_commands.command(
        name=locale_str("ping"), description=locale_str("Check the bot latency")
    )
    async def ping(self, interaction: discord.Interaction):
        embed = await self.service._ping(self, interaction)
