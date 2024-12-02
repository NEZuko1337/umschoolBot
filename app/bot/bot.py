import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app.bot.handlers.start import start_router
from app.bot.handlers.register import register_router
from app.bot.handlers.scores import scores_router
from dotenv import load_dotenv


load_dotenv()


async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start_router)
    dp.include_router(register_router)
    dp.include_router(scores_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
