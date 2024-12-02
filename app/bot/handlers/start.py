from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

start_router = Router()

@start_router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! Я помогу тебе зарегистрироваться и добавить баллы ЕГЭ.\n"
        "Используй команды:\n"
        "/register - для регистрации\n"
        "/enter_scores - для ввода баллов\n"
        "/view_scores - для просмотра баллов"
    )
