import asyncio
from datetime import timedelta

import discord
import pendulum
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot import Carbon
from app.db.cache.guild_cache import GuildCache
from app.db.services.caselog_service import CaseLogService
from app.db.session import session_maker
from app.i18n.marker import _
from app.utils.confs.enums import ActionType, ModLogAction
from app.utils.core.embed import Embed
from app.utils.helpers.check_target import TargetChecker
from app.utils.helpers.parse_time import parse_duration_to_timedelta


class ModCmdService:
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot

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
            return self.bot.log_embeds.dm_notification_embed(
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

    async def post_action_chores(
        self,
        interaction: discord.Interaction,
        target: discord.Member | discord.User,
        action_type: ActionType,
        mod_log_action: ModLogAction,
        reason: str,
        duration_str: str = "Permanent",
        duration_int: int = 0,
    ) -> None:
        assert interaction.guild is not None
        async with session_maker() as session, session.begin():
            dm_embed = await self.build_dm_embed(
                interaction.guild, mod_log_action, reason, duration_str, session=session
            )
            log_channel_id = await GuildCache.get_modlog_channel_id(
                self.bot, session, interaction.guild.id
            )

        async with session_maker() as session, session.begin():
            await self.create_case(
                interaction,
                target.id,
                action_type,
                reason,
                duration=duration_int,
                session=session,
            )

        if log_channel_id:
            log_channel = interaction.guild.get_channel(log_channel_id)
            if log_channel is None:
                try:
                    log_channel = await interaction.guild.fetch_channel(log_channel_id)
                except (discord.NotFound, discord.Forbidden):
                    log_channel = None

            if log_channel and isinstance(log_channel, discord.TextChannel):
                log_embed = self.bot.log_embeds.action_on_user(
                    mod_log_action, target, interaction.user, reason, duration_str
                )
                await log_channel.send(embed=log_embed)

        if dm_embed and isinstance(target, discord.Member):
            try:
                await target.send(embed=dm_embed)
            except Exception:
                self.bot.logger.error(f"DM failed for {action_type}: {Exception}")

    def fire_and_forget(self, coro):
        task = asyncio.create_task(coro)
        task.add_done_callback(
            lambda t: (
                self.bot.logger.error(f"Error in fire_and_forget: {t.exception()}")
                if t.exception()
                else None
            )
        )
        return task

    async def _kick(
        self, interaction: discord.Interaction, target: discord.Member, reason: str
    ) -> None:
        await interaction.response.defer(ephemeral=True)
        try:
            await target.kick(reason=f"{interaction.user.name} : {reason}")
        except discord.Forbidden:
            result = await self.validate_my_guy(interaction, target)
            if result is not None:
                await interaction.followup.send(embed=result, ephemeral=True)
                return
        except Exception as e:
            error_embed = self.bot.embed_factory.error_embed(_("Something went wrong."))
            self.bot.logger.error(f"Kick command failed : {e}")
            await interaction.followup.send(embed=error_embed, ephemeral=True)
            return

        success_embed = self.bot.embed_factory.success_embed(
            _("**%(user_mention)s** was kicked."), user_mention=target.name
        )
        await interaction.followup.send(embed=success_embed, ephemeral=True)
        self.fire_and_forget(
            self.post_action_chores(
                interaction, target, ActionType.KICK, ModLogAction.KICK, reason
            )
        )

    async def _ban(
        self, interaction: discord.Interaction, target: discord.Member, reason: str
    ) -> None:
        await interaction.response.defer(ephemeral=True)
        try:
            await target.ban(reason=f"{interaction.user.name} : {reason}")
        except discord.Forbidden:
            result = await self.validate_my_guy(interaction, target)
            if result is not None:
                await interaction.followup.send(embed=result, ephemeral=True)
                return
        except Exception as e:
            error_embed = self.bot.embed_factory.error_embed(_("Something went wrong."))
            self.bot.logger.error(f"Ban command failed : {e}")
            await interaction.followup.send(embed=error_embed, ephemeral=True)
            return

        success_embed = self.bot.embed_factory.success_embed(
            _("**%(user_mention)s** was banned."), user_mention=target.name
        )
        await interaction.followup.send(embed=success_embed, ephemeral=True)
        self.fire_and_forget(
            self.post_action_chores(
                interaction, target, ActionType.BAN, ModLogAction.BAN, reason
            )
        )

    async def _unban(
        self, interaction: discord.Interaction, user_id: str, reason: str
    ) -> None:
        await interaction.response.defer(ephemeral=True)
        assert interaction.guild is not None
        try:
            user = await self.bot.fetch_user(int(user_id))
            await interaction.guild.unban(
                user, reason=f"{interaction.user.name} : {reason}"
            )
        except (ValueError, discord.NotFound):
            error_embed = self.bot.embed_factory.error_embed(_("User not found."))
            await interaction.followup.send(embed=error_embed, ephemeral=True)
            return
        except discord.Forbidden:
            error_embed = self.bot.embed_factory.error_embed(
                _("I don't have permission to unban this user.")
            )
            await interaction.followup.send(embed=error_embed, ephemeral=True)
            return
        except Exception as e:
            error_embed = self.bot.embed_factory.error_embed(_("Something went wrong."))
            self.bot.logger.error(f"Unban command failed : {e}")
            await interaction.followup.send(embed=error_embed, ephemeral=True)
            return

        success_embed = self.bot.embed_factory.success_embed(
            _("**%(user_name)s** was unbanned."), user_name=user.name
        )
        await interaction.followup.send(embed=success_embed, ephemeral=True)

        # Unban chores (no DM possible as user is not in guild)
        async with session_maker() as session, session.begin():
            log_channel_id = await GuildCache.get_modlog_channel_id(
                self.bot, session, interaction.guild.id
            )
        if log_channel_id:
            log_channel = interaction.guild.get_channel(log_channel_id)
            if log_channel and isinstance(log_channel, discord.TextChannel):
                log_embed = self.bot.log_embeds.action_on_user(
                    ModLogAction.UNBAN, user, interaction.user, reason
                )
                await log_channel.send(embed=log_embed)

    async def _timeout(
        self,
        interaction: discord.Interaction,
        target: discord.Member,
        duration: str,
        reason: str,
    ) -> None:
        await interaction.response.defer(ephemeral=True)

        parsed_duration = parse_duration_to_timedelta(self.bot, duration)
        if isinstance(parsed_duration, Embed):
            await interaction.followup.send(embed=parsed_duration, ephemeral=True)
            return

        td = timedelta(seconds=parsed_duration.total_seconds())

        try:
            await target.timeout(td, reason=f"{interaction.user.name} : {reason}")
        except discord.Forbidden:
            result = await self.validate_my_guy(interaction, target)
            if result is not None:
                await interaction.followup.send(embed=result, ephemeral=True)
                return
        except Exception as e:
            error_embed = self.bot.embed_factory.error_embed(_("Something went wrong."))
            self.bot.logger.error(f"Timeout command failed : {e}")
            await interaction.followup.send(embed=error_embed, ephemeral=True)
            return

        duration_str = pendulum.now().add(seconds=td.total_seconds()).diff_for_humans()
        success_embed = self.bot.embed_factory.success_embed(
            _("**%(user_mention)s** was timed out for %(duration)s."),
            user_mention=target.name,
            duration=duration,
        )
        await interaction.followup.send(embed=success_embed, ephemeral=True)
        self.fire_and_forget(
            self.post_action_chores(
                interaction,
                target,
                ActionType.TIMEOUT,
                ModLogAction.TIMEOUT,
                reason,
                duration_str=duration_str,
                duration_int=int(td.total_seconds()),
            )
        )

    async def _warn(
        self, interaction: discord.Interaction, target: discord.Member, reason: str
    ) -> None:
        await interaction.response.defer(ephemeral=True)

        result = await self.validate_my_guy(interaction, target)
        if result is not None:
            await interaction.followup.send(embed=result, ephemeral=True)
            return

        success_embed = self.bot.embed_factory.success_embed(
            _("**%(user_mention)s** was warned."), user_mention=target.name
        )
        await interaction.followup.send(embed=success_embed, ephemeral=True)
        self.fire_and_forget(
            self.post_action_chores(
                interaction, target, ActionType.WARN, ModLogAction.WARN, reason
            )
        )
