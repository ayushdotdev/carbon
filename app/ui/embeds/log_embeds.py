from app.utils.confs.enums import ModLogAction
from app.utils.core.embed import Embed
from app.utils.helpers.embed_factory import EmbedFactory
from app.i18n.manager import I18nManager


class LogEmbed(EmbedFactory):
    def __init__(self, i18n: I18nManager) -> None:
        super().__init__(i18n)

    def base_log_embed(self, action: ModLogAction) -> Embed:
        embed = self._build()
        embed.set_title_i18n(action.title)
        return embed
