import discord
from discord import Interaction, app_commands
from discord.app_commands import locale_str
from discord.ext import commands

from app.bot import Carbon
from app.i18n.marker import _
from app.services.commands.general import GeneralService
from app.ui.views.invite_view import InviteView


class General(commands.Cog):
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot
        self.service = GeneralService(self.bot)

    # -- ping command --
    @app_commands.command(
        name="ping", description=locale_str(_("Check the bot latency."))
    )
    @app_commands.guild_only()
    async def ping(self, interaction: Interaction) -> None:
        embed = await self.service._ping(interaction)
        await interaction.response.send_message(embed=embed)

    # -- invite command --
    @app_commands.command(
        name="invite", description=locale_str(_("Get an invite link for Carbon."))
    )
    @app_commands.guild_only()
    async def invite(self, interaction: discord.Interaction) -> None:
        view = InviteView(interaction, timeout=60)
        embed = await self.service._invite(interaction)
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot: Carbon):
    await bot.add_cog(General(bot))
