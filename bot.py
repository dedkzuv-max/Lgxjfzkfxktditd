import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton
)

TOKEN = "8520830099:AAF5r2OaCaeK2lHWGdiaXp8LATcZnz3N6mU"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# =========================
# КНОПКИ
# =========================

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⭐ Заработать звёзды"),
            KeyboardButton(text="🎉 Задания")
        ],
        [
            KeyboardButton(text="🎁 Вывести звёзды")
        ],
        [
            KeyboardButton(text="✨ Активировать купон")
        ],
        [
            KeyboardButton(text="💎 Бонус")
        ],
        [
            KeyboardButton(text="👤 Профиль"),
            KeyboardButton(text="🏆 Топ")
        ]
    ],
    resize_keyboard=True
)

# =========================
# START
# =========================

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "⭐ Добро пожаловать!",
        reply_markup=menu
    )

# =========================
# КНОПКИ
# =========================

@dp.message()
async def buttons(message: Message):

    if message.text == "⭐ Заработать звёзды":
        await message.answer("⭐ Раздел заработка")

    elif message.text == "🎉 Задания":
        await message.answer("🎉 Раздел заданий")

    elif message.text == "🎁 Вывести звёзды":
        await message.answer("🎁 Раздел вывода")

    elif message.text == "✨ Активировать купон":
        await message.answer("✨ Отправьте купон")

    elif message.text == "💎 Бонус":
        await message.answer("💎 Ваш бонус")

    elif message.text == "👤 Профиль":
        await message.answer("👤 Ваш профиль")

    elif message.text == "🏆 Топ":
        await message.answer("🏆 Топ пользователей")

# =========================
# ЗАПУСК
# =========================

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
