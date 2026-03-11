from typing import Any

import discord

from app.bot import Carbon
from app.db.cache.guild_cache import GuildCache
from app.db.models.case_logs import CaseLog
from app.db.session import session_maker
from app.i18n.marker import _
from app.utils.confs.enums import ActionType
from app.utils.helpers.check_target import TargetChecker


class ModCmdService:
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot

    async def basic_mod_work(
        self,
        interaction: discord.Interaction,
        target: discord.Member,
        action: ActionType,
        reason: str,
    ) -> Any:
        checker = TargetChecker(self.bot, interaction, target)
        assert interaction.guild is not None
        validate = await checker.validate()

        if validate is not None:
            return validate

        async with session_maker() as session, session.begin():
            await CaseLog.add_log(
                session,
                interaction.guild.id,
                target.id,
                interaction.user.id,
                action,
                reason,
            )

    async def send_log_msg(self, guild: discord.Guild) -> None:
        async with session_maker() as session, session.begin():
            log_channel_id: int | None = await GuildCache.get_modlog_channel_id(
                self.bot, session, guild.id
            )

        if log_channel_id is not None:
            log_channel = await guild.fetch_channel(log_channel_id)

    async def _kick(
        self, interaction: discord.Interaction, target: discord.Member, reason: str
    ):
        assert interaction.guild is not None
        result = await self.basic_mod_work(interaction, target, ActionType.KICK, reason)

        if result is not None:
            return result

        try:
            await target.kick(reason=f"{interaction.user.name}: {reason}")
        except Exception:
            return self.bot.embed_factory.error_embed(_("Something went wrong"))
