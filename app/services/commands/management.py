import discord
from app.bot import Carbon
from app.i18n.marker import _


class ManagementService:
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot

    async def _purge(self, interaction: discord.Interaction, count: int) -> None:
        assert isinstance(interaction.channel, discord.TextChannel)
        deleted = await interaction.channel.purge(limit=count)

        embed = self.bot.embed_factory.success_embed(
            _("Deleted %(count)s messages."), count=deleted
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
