import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

TOKEN = "8799385592:AAEsPJ6vMXx0P5Eq_iSqXcUlyCvvW0szJwA"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# INLINE КНОПКИ
menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🌲 Купить Stars",
                callback_data="buy"
            ),
            InlineKeyboardButton(
                text="🌿 Рефералы",
                callback_data="refs"
            )
        ],
        [
            InlineKeyboardButton(
                text="🧮 Калькулятор",
                callback_data="calc"
            ),
            InlineKeyboardButton(
                text="✉️ Поддержка",
                url="https://t.me/Kuki_Star_Kz"
            )
        ],
        [
            InlineKeyboardButton(
                text="💬 Отзывы",
                url="https://t.me/"
            )
        ]
    ]
)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "🌲👋 Добро пожаловать в Kuki Stars!\n\n"
        "Самые дешевые звезды 💸\n"
        "Покупка от 50 ⭐",
        reply_markup=menu
    )

async def main():
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())