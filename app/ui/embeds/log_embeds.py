import discord

from app.i18n.manager import I18nManager
from app.i18n.marker import _
from app.utils.confs.enums import ModLogAction
from app.utils.core.embed import Embed
from app.utils.helpers.embed_factory import EmbedFactory


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
        return self.base_log_embed(action).set_description_i18n(
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

    def purge_messages_embed(
        self, message_count: int, moderator: discord.abc.User
    ) -> Embed:
        embed = self.base_log_embed(ModLogAction.PURGE)
        embed.set_description_i18n(
            _(
                "**Message Count:** %(message_count)s\n> **Moderator:** %(mod_name)s ( %(mod_id)s )"
            ),
            message_count=message_count,
            mod_id=moderator.id,
            mod_name=moderator.mention,
        )
        return embed

    def dm_notification_embed(
        self,
        action: ModLogAction,
        guild: discord.Guild,
        reason: str,
        duration: str = "Permanent",
    ) -> Embed:
        embed = self._build(color=action.color)
        if action.dm_title:
            embed.set_title_i18n(action.dm_title)
        embed.add_field_i18n(_("Reason"), _("%(reason)s"), reason=reason)
        embed.add_field_i18n(_("Duration"), _("%(duration)s"), duration=duration)
        embed.set_footer_i18n(_("Sent from %(guild_name)s"), guild_name=guild.name)
        embed.footer.icon_url = guild.icon.url if guild.icon else None

        return embed
