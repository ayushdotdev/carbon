import discord
from discord import app_commands

from app.bot import Carbon
from app.i18n.context import ExecutionContext
from app.i18n.marker import _
from app.utils.consts.perm_label import PERMISSION_LABELS
from app.utils.core.embed import Embed


class ErrorService:
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot

    async def _on_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ) -> Embed | None:
        ExecutionContext.set_context(interaction)

        if isinstance(error, app_commands.MissingPermissions):
            perms = ", ".join(
                PERMISSION_LABELS.get(p, p.replace("_", " "))
                for p in error.missing_permissions
            )
            embed = self.bot.embed_factory.error_embed(
                _("You don't have the required permissions to use this command.")
            )
            embed.add_field_i18n(_("Missing Permissions"), perms)

            return embed

        if isinstance(error, app_commands.BotMissingPermissions):
            perms = ", ".join(
                PERMISSION_LABELS.get(p, p.replace("_", " "))
                for p in error.missing_permissions
            )
            embed = self.bot.embed_factory.error_embed(
                _("I don't have the required permissions to run this command.")
            )
            embed.add_field_i18n(_("Missing Permissions"), perms)

            return embed

        return None
