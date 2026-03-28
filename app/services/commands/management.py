import discord
from app.bot import Carbon


class ManagementService:
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot

    async def _purge(self, interaction: discord.Interaction, count: int) -> None:
        assert isinstance(interaction.channel, discord.TextChannel)
        await interaction.channel.purge(limit=count)
