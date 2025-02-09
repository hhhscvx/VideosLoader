import logging
import asyncio

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from routers import router as main_router
from settings import settings


dp = Dispatcher()
dp.include_router(main_router)


async def main(bot: Bot):
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


if __name__ == "__main__":
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    asyncio.run(main(bot=bot))
