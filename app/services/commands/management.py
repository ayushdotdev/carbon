import discord

from app.bot import Carbon
from app.db.services.modsettings_service import ModSettingsService
from app.db.session import session_maker
from app.i18n.marker import _


class ManagementService:
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot

    async def _purge(self, interaction: discord.Interaction, count: int) -> None:
        assert isinstance(interaction.channel, discord.TextChannel)
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=count)

        embed = self.bot.embed_factory.success_embed(
            _("Deleted %(count)s messages."), count=len(deleted)
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

    async def _set_modlog_channel(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ) -> None:
        async with session_maker() as session, session.begin():
            assert interaction.guild is not None
            await ModSettingsService.set_log_channel_id(
                session, interaction.guild.id, channel.id
            )
        embed = self.bot.embed_factory.success_embed(
            _("Succesfully set %(channel_mention)s to receive moderation logs."),
            channel_mention=channel.mention,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
