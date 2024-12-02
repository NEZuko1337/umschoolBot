from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Создаем клавиатуру
main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/register")],
        [KeyboardButton(text="/enter_scores")],
        [KeyboardButton(text="/view_scores")]
    ],
    resize_keyboard=True
)
