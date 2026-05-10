import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    FSInputFile
)

TOKEN = "8799385592:AAEsPJ6vMXx0P5Eq_iSqXcUlyCvvW0szJwA"

bot = Bot(token=TOKEN)
dp = Dispatcher()

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

@dp.message(CommandStart())
async def start(message: Message):

    video = FSInputFile("video.mp4")  # видео должно лежать рядом с bot.py

    await message.answer_video(
        video=video,
        caption=(
            "🌲👋 Добро пожаловать в Kuki Stars!\n\n"
            "Самые дешевые звезды💸\n"
            "Покупка от 50 ⭐"
        ),
        reply_markup=menu
    )

async def main():
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())