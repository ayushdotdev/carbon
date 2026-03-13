import discord
from discord import app_commands
from discord.ext import commands

from app.bot import Carbon
from app.i18n.marker import _
from app.services.commands.moderation import ModCmdService


class ModerationCog(commands.Cog):
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot
        self.service = ModCmdService(self.bot)

    @app_commands.command(
        name="kick",
        description=app_commands.locale_str(_("Kick someone from this server.")),
    )
    @app_commands.guild_only()
    @app_commands.checks.bot_has_permissions(kick_members=True)
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(
        self,
        interaction: discord.Interaction,
        target: discord.Member,
        reason: str = "No reason provided.",
    ):
        await self.service._kick(interaction, target, reason)
