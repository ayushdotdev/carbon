from typing import Any, Self
import discord
from app.helpers.enums import LocaleType
from app.i18n.manager import I18nManager


class Embed(discord.Embed):
    def __init__(
        self,
        *,
        i18n: I18nManager,
        locale: discord.Locale | None = None,
        locale_type: LocaleType = LocaleType.user,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.i18n = i18n
        self.locale = locale
        self.locale_type = locale_type

    def set_title_i18n(self, msgid: str, **params: Any) -> Self:
        self.title = self.i18n.gettext(
            msgid,
            locale_type=self.locale_type,
            locale=self.locale,
            **params,
        )
        return self

    def set_description_i18n(self, msgid: str, **params: Any) -> Self:
        self.description = self.i18n.gettext(
            msgid,
            locale_type=self.locale_type,
            locale=self.locale,
            **params,
        )
        return self

    def add_field_i18n(
        self, name_id: str, value_id: str, *, inline: bool = True, **params: Any
    ) -> Self:
        name = self.i18n.gettext(
            name_id, locale_type=self.locale_type, locale=self.locale, **params
        )
        value = self.i18n.gettext(
            value_id, locale_type=self.locale_type, locale=self.locale, **params
        )
        super().add_field(name=name, value=value, inline=inline)
        return self

    def set_footer_i18n(
        self, text_id: str, *, icon_url: str | None = None, **params: Any
    ) -> Self:
        text = self.i18n.gettext(
            text_id, locale_type=self.locale_type, locale=self.locale, **params
        )
        super().set_footer(text=text, icon_url=icon_url)
        return self
