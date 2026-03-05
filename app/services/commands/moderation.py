import discord
from app.bot import Carbon
from app.utils.core.embed import Embed
from app.utils.helpers.check_target import TargetChecker

class ModCmdService:
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot

    async def basics(self, interaction: discord.Interaction, target: discord.Member) -> Embed | None:
        checker = TargetChecker(self.bot, interaction,target)
        return await checker.validate()

    async def _kick(self, interaction: discord.Interaction, target: discord.Member, reason: str):
        result = await self.basics(interaction, target)
        
        if result:
            return result
        
        
