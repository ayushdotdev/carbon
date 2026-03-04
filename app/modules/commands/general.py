from discord import Interaction, app_commands
from discord.app_commands import locale_str
from discord.ext import commands

from app.bot import Carbon
from app.i18n.marker import _
from app.services.commands.general import GeneralService


class General(commands.Cog):
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot
        self.service = GeneralService(self.bot)

    @app_commands.command(
        name="ping", description=locale_str(_("Check the bot latency."))
    )
    @app_commands.guild_only()
    async def ping(self, interaction: Interaction) -> None:
        embed = await self.service._ping(interaction)
        await interaction.response.send_message(embed=embed)


async def setup(bot: Carbon):
    await bot.add_cog(General(bot))
