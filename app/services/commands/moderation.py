import discord
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot import Carbon
from app.db.cache.guild_cache import GuildCache
from app.db.services.caselog_service import CaseLogService
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
        return checker.validate()

    async def get_log_channel(
        self, guild: discord.Guild, session: AsyncSession | None = None
    ) -> discord.TextChannel | None:
        if session is None:
            async with session_maker() as session, session.begin():
                log_channel_id: int | None = await GuildCache.get_modlog_channel_id(
                    self.bot, session, guild.id
                )
        else:
            log_channel_id: int | None = await GuildCache.get_modlog_channel_id(
                self.bot, session, guild.id
            )

        if log_channel_id is not None:
            log_channel = guild.get_channel(log_channel_id)
            if log_channel is None:
                try:
                    log_channel = await guild.fetch_channel(log_channel_id)
                except (discord.NotFound, discord.Forbidden):
                    return None
            assert isinstance(log_channel, discord.TextChannel)
            return log_channel
        return None

    async def build_dm_embed(
        self,
        guild: discord.Guild,
        action: ModLogAction,
        reason: str,
        duration: str = "Permanent",
        session: AsyncSession | None = None,
    ) -> Embed | None:
        if session is None:
            async with session_maker() as session, session.begin():
                is_dm_enabled = await GuildCache.get_if_dm_enabled(
                    self.bot, session, guild.id
                )
        else:
            is_dm_enabled = await GuildCache.get_if_dm_enabled(
                self.bot, session, guild.id
            )

        if is_dm_enabled:
            return self.log_embeds.dm_notification_embed(
                action, guild, reason, duration
            )
        return None

    async def create_case(
        self,
        interaction: discord.Interaction,
        target_id: int,
        action: ActionType,
        reason: str,
        *,
        duration: int = 0,
        session: AsyncSession | None = None,
    ) -> int:
        assert interaction.guild is not None
        if session is None:
            async with session_maker() as session, session.begin():
                return await CaseLogService.create_new_case(
                    session,
                    interaction.guild.id,
                    target_id,
                    interaction.user.id,
                    action,
                    reason,
                    duration,
                )
        else:
            return await CaseLogService.create_new_case(
                session,
                interaction.guild.id,
                target_id,
                interaction.user.id,
                action,
                reason,
                duration,
            )

    async def _kick(
        self, interaction: discord.Interaction, target: discord.Member, reason: str
    ) -> None:
        await interaction.response.defer(ephemeral=True)
        assert interaction.guild is not None
        result = await self.validate_my_guy(interaction, target)

        if result is not None:
            await interaction.followup.send(embed=result, ephemeral=True)
            return

        target_id = target.id
        guild = interaction.guild

        try:
            await target.kick(reason=f"{interaction.user.name} : {reason}")
        except Exception as e:
            error_embed = self.bot.embed_factory.error_embed(_("Something went wrong."))
            self.bot.logger.error(f"Kick command failed : {e}")
            await interaction.followup.send(embed=error_embed, ephemeral=True)
            return

        success_embed = self.bot.embed_factory.success_embed(
            _("**%(user_mention)s** was kicked."), user_mention=target.name
        )
        await interaction.followup.send(embed=success_embed, ephemeral=True)

        async with session_maker() as session, session.begin():
            dm_embed = await self.build_dm_embed(
                guild, ModLogAction.KICK, reason, session=session
            )
            log_channel_id = await GuildCache.get_modlog_channel_id(
                self.bot, session, guild.id
            )

        async with session_maker() as session, session.begin():
            await self.create_case(
                interaction, target_id, ActionType.KICK, reason, session=session
            )

            if log_channel_id:
                log_channel = guild.get_channel(log_channel_id)
                if log_channel is None:
                    try:
                        log_channel = await guild.fetch_channel(log_channel_id)
                    except (discord.NotFound, discord.Forbidden):
                        log_channel = None

                if log_channel and isinstance(log_channel, discord.TextChannel):
                    log_embed = self.log_embeds.action_on_user(
                        ModLogAction.KICK, target, interaction.user, reason
                    )
                    await log_channel.send(embed=log_embed)

        if dm_embed:
            try:
                await target.send(embed=dm_embed)
            except Exception:
                self.bot.logger.error(f"DM failed for kick: {Exception}")
