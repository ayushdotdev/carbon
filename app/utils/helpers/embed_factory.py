from typing import Any

import discord

from app.utils.consts.branding import (
    DEFAULT_CLR,
    ERROR_CLR,
    ERROR_EMOJI,
    SUCCESS_CLR,
    SUCCESS_EMOJI,
)
from app.utils.core.embed import Embed
from app.utils.confs.enums import LocaleType
from app.i18n.manager import I18nManager
from app.i18n.marker import _


class EmbedFactory:
    def __init__(self, i18n: I18nManager) -> None:
        self.i18n = i18n

    def _build(
        self,
        msgid: str | None = None,
        *,
        color: int = DEFAULT_CLR,
        local_type: LocaleType = LocaleType.USER,
        locale: discord.Locale | None = None,
        **params: Any,
    ) -> Embed:
        embed = Embed(
            i18n=self.i18n, locale=locale, locale_type=local_type, color=color
        )
        if msgid:
            embed.set_description_i18n(msgid, **params)
        return embed

    def success_embed(
        self,
        msgid: str,
        *,
        locale_type: LocaleType = LocaleType.USER,
        locale: discord.Locale | None = None,
        **params: Any,
    ) -> Embed:
        embed = self._build(
            msgid, color=SUCCESS_CLR, local_type=locale_type, locale=locale, **params
        ).set_title_i18n(
            _("%(success_emoji)s Action Completed"), success_emoji=SUCCESS_EMOJI
        )
        return embed

    def error_embed(
        self,
        msgid: str,
        *,
        locale_type: LocaleType = LocaleType.USER,
        locale: discord.Locale | None = None,
        **params: Any,
    ) -> Embed:
        return self._build(
            msgid, color=ERROR_CLR, local_type=locale_type, locale=locale, **params
        ).set_title_i18n(_("%(error_emoji)s Action Failed"), error_emoji=ERROR_EMOJI)
