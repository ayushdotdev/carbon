import discord

from app.bot import Carbon
from app.db.cache.guild_cache import GuildCache
from app.db.models.case_logs import CaseLog
from app.db.session import session_maker
from app.i18n.marker import _
from app.ui.embeds.log_embeds import LogEmbed
from app.utils.confs.enums import ActionType, ModLogAction
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

    async def _kick(
        self, interaction: discord.Interaction, target: discord.Member, reason: str
    ):
        assert interaction.guild is not None
        result = await self.validate_my_guy(interaction, target)

        if result is not None:
            await interaction.response.send_message(embed=result)

        log_channel = await self.get_log_channel(interaction.guild)

        if log_channel:
            log_embed = self.log_embeds.action_on_user(
                ModLogAction.KICK, target, interaction.user, reason
            )
            await log_channel.send(embed=log_embed)

        try:
            await target.kick(reason=f"{interaction.user.name}: {reason}")
            embed = self.bot.embed_factory.success_embed(
                _("**%(user_mention)** was kicked"), user_mention=target.global_name
            )
            await interaction.response.send_message(embed=embed)
        except Exception:
            return self.bot.embed_factory.error_embed(_("Something went wrong"))
