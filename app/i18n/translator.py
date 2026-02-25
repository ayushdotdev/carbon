from typing import Any
from discord import app_commands
import discord


class Translator(app_commands.Translator):
    def __init__(self, i18n) -> None:
        self.i18n = i18n
        super().__init__()

    async def translate(
        self,
        string: app_commands.locale_str,
        locale: discord.Locale,
        context: app_commands.TranslationContext[Any, Any],
    ) -> str | None:
        return self.i18n.gettext(string.message, locale=locale, **string.extras)
