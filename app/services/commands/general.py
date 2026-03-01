import discord
from app.helpers.embed import Embed
from app.bot import Carbon
from app.i18n.marker import _
from app.i18n.context import ExecutionContext


class GeneralService:
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot

    async def _ping(self, interaction: discord.Interaction) -> Embed:
        ExecutionContext.set(
            ExecutionContext(
                user_locale=interaction.locale,
                guild_locale=interaction.guild_locale,
            )
        )

        latency = round(self.bot.latency * 1000)

        embed = self.bot.embed_factory._build(
            _("Latency: %(latency)s ms."), latency=latency
        )

        return embed
