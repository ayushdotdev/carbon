import asyncio
import contextlib

from app.bot import Carbon
from app.utils.confs.logging import setup_logging

setup_logging()
bot = Carbon()


async def main() -> None:
    async with bot:
        await bot.start()


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
