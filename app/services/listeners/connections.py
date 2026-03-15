import discord

from app.bot import Carbon


class ConnectionService:
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot

    async def _on_ready(self):
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="/help")
        )
        self.bot.logger.info(f"Logged in as {self.bot.user}")
