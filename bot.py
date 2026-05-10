import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton
)

TOKEN = "8799385592:AAEsPJ6vMXx0P5Eq_iSqXcUlyCvvW0szJwA"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# КНОПКИ КАК НА ФОТО
menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🌲 Купить Stars"),
            KeyboardButton(text="🌿 Рефералы")
        ],
        [
            KeyboardButton(text="🧮 Калькулятор"),
            KeyboardButton(text="✉️ Поддержка")
        ],
        [
            KeyboardButton(text="💬 Отзывы")
        ]
    ],
    resize_keyboard=True
)

# START
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer_video(
        video="https://files.catbox.moe/7l6kz1.mp4",  # сюда своё видео
        caption=(
            "🌲👋 Добро пожаловать в Kuki Stars!\n\n"
            "Самые дешевые звезды 💸\n"
            "Покупка от 50 ⭐"
        ),
        reply_markup=menu
    )

# ЗАПУСК
async def main():
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())