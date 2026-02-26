from typing import Any
import discord
from app.helpers.enums import LocaleType
from app.i18n.manager import I18nManager
from app.helpers.constants import SUCCESS_CLR, DEFAULT_CLR, ERROR_CLR, INFO_CLR
from app.helpers.embed import Embed


class EmbedFactory:
    def __init__(self, i18n: I18nManager) -> None:
        self.i18n = i18n

    def _build(
        self,
        msgid: str,
        *,
        color: int = DEFAULT_CLR,
        local_type: LocaleType = LocaleType.user,
        locale: discord.Locale | None = None,
        **params: Any,
    ) -> Embed:
        embed = Embed(
            i18n=self.i18n, locale=locale, locale_type=local_type, color=color
        ).set_description_i18n(msgid=msgid, **params)
        return embed

    def success_embed(
        self,
        msgid: str,
        *,
        locale_type: LocaleType = LocaleType.user,
        locale: discord.Locale | None = None,
        **params: Any,
    ) -> Embed:
        return self._build(
            msgid, color=SUCCESS_CLR, local_type=locale_type, locale=locale, **params
        )

    def error_embed(
        self,
        msgid: str,
        *,
        locale_type: LocaleType = LocaleType.user,
        locale: discord.Locale | None = None,
        **params: Any,
    ) -> Embed:
        return self._build(
            msgid, color=ERROR_CLR, local_type=locale_type, locale=locale, **params
        )
