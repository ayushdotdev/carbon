import discord
from discord.ext import commands

import structlog
import os

from app.db.session import engine

from app.config import settings

from app.helpers.custom_tree import CustomCommandTree
from app.i18n.translator import Translator
from app.i18n.manager import I18nManager


class Carbon(commands.Bot):
    def __init__(self, *, debug: bool = False, **kwargs):
        self.i18n = I18nManager()
        self.tree: CustomCommandTree

        self.debug = debug
        self.logger = structlog.get_logger().bind(component="bot")

        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True

        discord.VoiceClient.warn_nacl = False

        super().__init__(
            command_prefix="!",
            help_command=None,
            intents=intents,
            tree_cls=CustomCommandTree,
            **kwargs,
        )

    async def setup_hook(self) -> None:
        self.logger.info("Running setup.....")
        await self.setup_modules()
        await self.init_i18n()
        self.logger.info("Setup completed, starting bot")

    async def init_i18n(self) -> None:
        await self.tree.set_translator(Translator(self.i18n))
        self.logger.info("I18n Setup completed")

    async def start(self, token: str | None = None, *, reconnect: bool = True) -> None:
        token = settings.bot_token
        self.logger.info("Launching Carbon")
        await super().start(token=token, reconnect=reconnect)

    async def close(self) -> None:
        await super().close()
        await engine.dispose()

    async def setup_modules(self) -> None:
        groups = ["app/modules/listeners", "app/modules/commands"]

        for group in groups:
            for cog in os.listdir(group):
                if cog.endswith(".py") and cog != "__init__.py":
                    path = cog[-3]
                    extension = f"{cog.replace('/', '.')}.{path}"

                    try:
                        await self.load_extension(extension)
                        self.logger.info(f"Loaded extension: {path}")
                    except Exception:
                        self.logger.error(f"Failed to load {path}: {Exception}")
