import discord
from discord import app_commands

from app.bot import Carbon
from app.i18n.context import ExecutionContext
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

            return self.bot.error_embeds.missing_perms_embed(perms)

        if isinstance(error, app_commands.BotMissingPermissions):
            perms = ", ".join(
                PERMISSION_LABELS.get(p, p.replace("_", " "))
                for p in error.missing_permissions
            )

            return self.bot.error_embeds.bot_missing_perms_embed(perms)

        return None
