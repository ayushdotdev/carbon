import discord
from app.utils.confs.enums import ModLogAction
from app.utils.core.embed import Embed
from app.utils.helpers.embed_factory import EmbedFactory
from app.i18n.manager import I18nManager
from app.i18n.marker import _


class LogEmbed(EmbedFactory):
    def __init__(self, i18n: I18nManager) -> None:
        super().__init__(i18n)

    def base_log_embed(self, action: ModLogAction) -> Embed:
        embed = self._build()
        embed.set_title_i18n(action.title)
        return embed

    def action_on_user(
        self,
        action: ModLogAction,
        target: discord.abc.User,
        moderator: discord.abc.User,
        reason: str,
        duration: str = "Permanent",
    ) -> Embed:
        embed = self.base_log_embed(action).set_description_i18n(
            _(
                "**User:** %(target_name)s ( %(target_id)s )\n> **Moderator:** %(mod_name)s ( %(mod_id)s )\n> **Reason:** %(reason)s\n> **Duration:** %(duration)s"
            ),
            target_name=target.mention,
            target_id=target.id,
            mod_name=moderator.mention,
            mod_id=moderator.id,
            reason=reason,
            duration=duration,
        )
        return embed
