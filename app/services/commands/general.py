import discord

from app.bot import Carbon
from app.i18n.context import ExecutionContext
from app.i18n.marker import _
from app.ui.views.invite_view import InviteView


class GeneralService:
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot

    async def _ping(self, interaction: discord.Interaction) -> None:
        ExecutionContext.set_context(interaction)

        latency = round(self.bot.latency * 1000)

        embed = self.bot.embed_factory._build().add_field_i18n(
            _("Latency"), _("%(latency)s ms"), latency=latency
        )

        await interaction.response.send_message(embed=embed)

    async def _invite(self, interaction: discord.Interaction) -> None:
        ExecutionContext.set_context(interaction)
        embed = self.bot.embed_factory._build(
            _("Click the button below to invite the bot to your server.")
        )
        embed.set_title_i18n(_("Thank you for taking interest in Carbon"))

        view = InviteView(interaction)
        await interaction.response.send_message(embed=embed, view=view)
