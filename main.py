import asyncio

from app.bot import Carbon
from app.helpers.logging import setup_logging

bot = Carbon()


async def main() -> None:
    async with bot:
        setup_logging()
        await bot.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
