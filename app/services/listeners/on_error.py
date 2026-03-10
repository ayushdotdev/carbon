import discord
from discord import app_commands

from app.i18n.context import ExecutionContext
from app.i18n.manager import I18nManager
from app.ui.embeds.error_embed import ErrorEmbed
from app.utils.consts.perm_label import PERMISSION_LABELS
from app.utils.core.embed import Embed


class ErrorService:
    def __init__(self) -> None:
        self.i18n = I18nManager()
        self.embeds = ErrorEmbed(self.i18n)

    async def _on_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ) -> Embed | None:
        ExecutionContext.set_context(interaction)

        if isinstance(error, app_commands.MissingPermissions):
            perms = ", ".join(
                PERMISSION_LABELS.get(p, p.replace("_", " "))
                for p in error.missing_permissions
            )

            embed = self.embeds.missing_perms_embed(perms)
            return embed

        if isinstance(error, app_commands.BotMissingPermissions):
            perms = ", ".join(
                PERMISSION_LABELS.get(p, p.replace("_", " "))
                for p in error.missing_permissions
            )

            embed = self.embeds.bot_missing_perms_embed(perms)
            return embed

        return None
