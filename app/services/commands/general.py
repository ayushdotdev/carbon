import discord

from app.bot import Carbon
from app.helpers.embed import Embed
from app.i18n.context import ExecutionContext
from app.i18n.marker import _


class GeneralService:
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot

    async def _ping(self, interaction: discord.Interaction) -> Embed:
        ExecutionContext.set_context(interaction)

        latency = round(self.bot.latency * 1000)

        embed = self.bot.embed_factory._build().add_field_i18n(
            _("Latency"), _("%(latency)s ms"), latency=latency
        )

        return embed
