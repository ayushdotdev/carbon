from app.bot import Carbon


class ConnectionService:
    def __init__(self, bot: Carbon) -> None:
        self.bot = bot

    async def _on_ready(self):
        await self.bot.init_guild()
        await self.bot.tree.sync()
