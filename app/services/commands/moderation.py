import discord
from app.bot import Carbon
from app.db.models.case_logs import CaseLog
from app.db.session import session_maker
from app.utils.confs.enums import ActionType
from app.i18n.marker import _
from app.utils.core.embed import Embed
from app.utils.helpers.check_target import TargetChecker


class ModCmdService:
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot

    async def basics(
        self, interaction: discord.Interaction, target: discord.Member
    ) -> Embed | None:
        checker = TargetChecker(self.bot, interaction, target)
        return await checker.validate()

    async def _kick(
        self, interaction: discord.Interaction, target: discord.Member, reason: str
    ):
        assert interaction.guild is not None
        result = await self.basics(interaction, target)

        if result:
            return result

        async with session_maker() as session, session.begin():
            await CaseLog.add_log(
                session,
                interaction.guild.id,
                target.id,
                interaction.user.id,
                ActionType.KICK,
                reason,
            )

        try:
            await target.kick(reason=f"{interaction.user.name}: {reason}")
        except Exception:
            return self.bot.embed_factory.error_embed(_("Something went wrong"))
