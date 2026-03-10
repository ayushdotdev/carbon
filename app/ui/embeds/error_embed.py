from app.i18n.manager import I18nManager
from app.i18n.marker import _
from app.utils.core.embed import Embed
from app.utils.helpers.embed_factory import EmbedFactory


class ErrorEmbed(EmbedFactory):
    def __init__(self, i18n: I18nManager) -> None:
        super().__init__(i18n)

    def missing_perms_embed(self, perms: str) -> Embed:
        embed = self.error_embed(
            _("You don't have the required permissions to use this command.")
        )
        embed.add_field_i18n(_("Missing Permissions"), perms)

        return embed

    def bot_missing_perms_embed(self, perms: str) -> Embed:
        embed = self.error_embed(
            _("I don't have the required permissions to run this command.")
        )
        embed.add_field_i18n(_("Missing Permissions"), perms)

        return embed
