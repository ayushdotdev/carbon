import discord
from discord import app_commands
from discord.ext import commands

from app.bot import Carbon
from app.i18n.marker import _
from app.services.commands.moderation import ModCmdService


class Moderation(commands.Cog):
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

    @app_commands.command(
        name="ban",
        description=app_commands.locale_str(_("Ban someone from this server.")),
    )
    @app_commands.guild_only()
    @app_commands.checks.bot_has_permissions(ban_members=True)
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        target: discord.Member,
        reason: str = "No reason provided.",
    ):
        await self.service._ban(interaction, target, reason)

    @app_commands.command(
        name="unban",
        description=app_commands.locale_str(_("Unban someone from this server.")),
    )
    @app_commands.guild_only()
    @app_commands.checks.bot_has_permissions(ban_members=True)
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(
        self,
        interaction: discord.Interaction,
        user_id: str,
        reason: str = "No reason provided.",
    ):
        await self.service._unban(interaction, user_id, reason)

    @app_commands.command(
        name="timeout",
        description=app_commands.locale_str(_("Timeout someone in this server.")),
    )
    @app_commands.guild_only()
    @app_commands.checks.bot_has_permissions(moderate_members=True)
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(
        self,
        interaction: discord.Interaction,
        target: discord.Member,
        duration: str,
        reason: str = "No reason provided.",
    ):
        await self.service._timeout(interaction, target, duration, reason)

    @app_commands.command(
        name="warn",
        description=app_commands.locale_str(_("Warn a member of this server.")),
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warn(
        self,
        interaction: discord.Interaction,
        target: discord.Member,
        reason: str = "No reason provided.",
    ):
        await self.service._warn(interaction, target, reason)


async def setup(bot: Carbon):
    await bot.add_cog(Moderation(bot))
