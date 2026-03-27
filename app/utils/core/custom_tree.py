from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING

import discord
from discord import app_commands

from app.i18n.context import ExecutionContext

if TYPE_CHECKING:
    from app.bot import Carbon


class CustomCommandTree(app_commands.CommandTree):
    def __init__(self, bot: "Carbon"):
        super().__init__(bot)
        self._global_checks: list[
            Callable[[discord.Interaction], bool | Awaitable[bool]]
        ] = []

    def add_check(
        self, check: Callable[[discord.Interaction], bool | Awaitable[bool]]
    ) -> None:
        self._global_checks.append(check)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        ExecutionContext.set_context(interaction)

        for check in self._global_checks:
            result = check(interaction)

            if isinstance(result, Awaitable):
                result = await result

            if not result:
                raise app_commands.CheckFailure()

        return True
