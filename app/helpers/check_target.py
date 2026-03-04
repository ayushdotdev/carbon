import discord

from app.bot import Carbon
from app.helpers.embed import Embed
from app.i18n.marker import _


class TargetChecker:
    def __init__(
        self, bot: Carbon, interaction: discord.Interaction, target: discord.Member
    ) -> None:
        self.bot = bot
        self.interaction = interaction
        self.guild = interaction.guild
        assert self.guild is not None
        self.target = target
        self.author = interaction.user
        self.bot_member = self.guild.me

        assert isinstance(self.author, discord.Member)

    def _role_position(self, member: discord.Member) -> int:
        return member.top_role.position if member.top_role else -1

    def validate(self) -> Embed | None:
        if self.target.id == self.interaction.client.user.id:
            return self.bot.embed_factory.error_embed(
                _("This action cannot be performed.")
            )
        if self.target.id == self.guild.owner_id:
            return self.bot.embed_factory.error_embed(
                _("The server owner cannot be targeted.")
            )
        if self.target.id == self.author.id:
            return self.bot.embed_factory.error_embed(
                _("This action cannot be performed on yourself.")
            )
        if target.bot:
            return self.bot.embed_factory.error_embed(
                _("Bots cannot be targeted with this action.")
            )

        bot_top = self._role_position(self.bot_member)
        target_top = self._role_position(self.target)
        author_top = self._role_position(self.author)

        if target_top >= bot_top:
            return self.bot.embed_factory.error_embed(
                _("My role must be higher than the target's role.")
            )
        if target_top >= author_top and self.author.id != self.guild.owner_id:
            return self.bot.embed_factory.error_embed(
                _("Your role must be higher than the target's role.")
            )
