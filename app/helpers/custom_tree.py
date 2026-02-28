from typing import Awaitable, Callable
import discord
from discord import app_commands


class CustomCommandTree(app_commands.CommandTree):
    def __init__(self, client: discord.Client):
        super().__init__(client)
        self._global_checks: list[
            Callable[[discord.Interaction], bool | Awaitable[bool]]
        ] = []

    def add_check(
        self, check: Callable[[discord.Interaction], bool | Awaitable[bool]]
    ) -> None:
        self._global_checks.append(check)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        for check in self._global_checks:
            result = check(interaction)

            if isinstance(result, Awaitable):
                result = await result

            if not result:
                raise app_commands.CheckFailure()

        return True
