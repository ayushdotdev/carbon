import contextvars
from typing import Optional

import discord

_current_ctx = contextvars.ContextVar("execution_context")


class ExecutionContext:
    def __init__(
        self,
        user_locale: discord.Locale | None = None,
        guild_locale: discord.Locale | None = None,
    ) -> None:
        self.user_locale = user_locale
        self.guild_locale = guild_locale

    @classmethod
    def set(cls, ctx: "ExecutionContext"):
        _current_ctx.set(ctx)

    @classmethod
    def get(cls) -> Optional["ExecutionContext"]:
        try:
            return _current_ctx.get()
        except LookupError:
            return None
