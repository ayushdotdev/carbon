import discord
from discord import app_commands
from discord.ext import commands

from app.bot import Carbon
from app.i18n.marker import _
from app.services.commands.management import ManagementService


class Management(commands.Cog):
    def __init__(self, bot: Carbon):
        self.bot = bot
        self.service = ManagementService(self.bot)

    @app_commands.command(
        name="purge", description=app_commands.locale_str(_("Delete messages in bulk."))
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    @app_commands.describe(
        count=app_commands.locale_str(_("The max number of messages to get deleted."))
    )
    async def purge(self, interaction: discord.Interaction, count: int) -> None:
        await self.service._purge(interaction, count)


async def setup(bot: Carbon):
    await bot.add_cog(Management(bot))
