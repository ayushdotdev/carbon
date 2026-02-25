import gettext
from gettext import GNUTranslations, NullTranslations
import discord

from app.i18n.context import ExecutionContext
from app.helpers.enums import LocaleType


class I18nManager:
    def __init__(self, locale_dir: str = "locales", domain: str = "messages") -> None:
        self.locale_dir = locale_dir
        self.domain = domain
        self._cache: dict[str, GNUTranslations | NullTranslations] = {}

    def _load(self, locale: str):
        try:
            return gettext.translation(
                self.domain, localedir=self.locale_dir, languages=[locale]
            )
        except FileNotFoundError:
            return gettext.translation(
                self.domain, localedir=self.locale_dir, languages=["en"]
            )

    def _resolve_locale(
        self, locale: discord.Locale | None, locale_type: LocaleType
    ) -> str:
        if locale:
            return locale.value

        ctx = ExecutionContext.get()
        if ctx:
            if locale_type == LocaleType.user and ctx.user_locale:
                return ctx.user_locale.value
            if locale_type == LocaleType.guild and ctx.guild_locale:
                return ctx.guild_locale.value

        return "en"

    def _get_translation(self, locale: str):
        if locale not in self._cache:
            self._cache[locale] = self._load(locale)
        return self._cache[locale]

    def gettext(
        self,
        msgid: str,
        *,
        locale_type: LocaleType = LocaleType.user,
        locale: discord.Locale | None = None,
        **kwargs,
    ) -> str:
        resolved = self._resolve_locale(locale, locale_type)
        tr = self._get_translation(resolved)
        return tr.gettext(msgid) % kwargs

    def ngettext(
        self,
        singular: str,
        plural: str,
        n: int,
        *,
        locale_type: LocaleType = LocaleType.user,
        locale: discord.Locale | None = None,
        **kwargs,
    ) -> str:
        resolved = self._resolve_locale(locale, locale_type)
        tr = self._get_translation(resolved)
        return tr.ngettext(singular, plural, n) % kwargs
