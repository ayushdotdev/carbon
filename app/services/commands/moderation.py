import discord

from app.bot import Carbon
from app.db.cache.guild_cache import GuildCache
from app.db.session import session_maker
from app.i18n.marker import _
from app.ui.embeds.log_embeds import LogEmbed
from app.utils.confs.enums import ModLogAction
from app.utils.core.embed import Embed
from app.utils.helpers.check_target import TargetChecker


class ModCmdService:
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot
        self.log_embeds = LogEmbed(self.bot.i18n)

    async def validate_my_guy(
        self, interaction: discord.Interaction, target: discord.Member
    ) -> Embed | None:
        checker = TargetChecker(self.bot, interaction, target)
        assert interaction.guild is not None
        validate = await checker.validate()

        if validate is not None:
            return validate
        return None

    async def get_log_channel(self, guild: discord.Guild) -> discord.TextChannel | None:
        async with session_maker() as session, session.begin():
            log_channel_id: int | None = await GuildCache.get_modlog_channel_id(
                self.bot, session, guild.id
            )

        if log_channel_id is not None:
            log_channel = await guild.fetch_channel(log_channel_id)
            assert isinstance(log_channel, discord.TextChannel)
            return log_channel
        return None

    async def send_dm(
        self,
        guild: discord.Guild,
        target: discord.Member,
        action: ModLogAction,
        reason: str,
        duration: str = "Permanent",
    ) -> None:
        async with session_maker() as session, session.begin():
            is_dm_enabled = await GuildCache.get_if_dm_enabled(
                self.bot, session, guild.id
            )

            if is_dm_enabled:
                embed = self.log_embeds.dm_notification_embed(
                    action, guild, reason, duration
                )
                await target.send(embed=embed)

    async def _kick(
        self, interaction: discord.Interaction, target: discord.Member, reason: str
    ):
        await interaction.response.defer()
        assert interaction.guild is not None
        result = await self.validate_my_guy(interaction, target)

        if result is not None:
            await interaction.followup.send(embed=result, ephemeral=True)
            return

        try:
            await target.kick(reason=f"{interaction.user.name}: {reason}")
        except Exception as e:
            embed = self.bot.embed_factory.error_embed(_("Something went wrong."))
            self.bot.logger.error(f"Kick command failed : {e}")
            await interaction.followup.send(embed=embed)
            return
        embed = self.bot.embed_factory.success_embed(
            _("**%(user_mention)s** was kicked."), user_mention=target.global_name
        )

        try:
            await self.send_dm(interaction.guild, target, ModLogAction.KICK, reason)
        except Exception as e:
            embed.add_field_i18n(_("Error"), _("The user did not receive a dm."))

        await interaction.followup.send(embed=embed, ephemeral=True)

        log_channel = await self.get_log_channel(interaction.guild)

        if log_channel is not None:
            log_embed = self.log_embeds.action_on_user(
                ModLogAction.KICK, target, interaction.user, reason
            )
            await log_channel.send(embed=log_embed)
