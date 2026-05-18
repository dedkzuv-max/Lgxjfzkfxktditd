import asyncio
import sqlite3

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton
)

# =========================================
# НАСТРОЙКИ
# =========================================

TOKEN = "8520830099:AAF5r2OaCaeK2lHWGdiaXp8LATcZnz3N6mU"
ADMIN_ID = 8520830099

bot = Bot(token=TOKEN)
dp = Dispatcher()

# =========================================
# DATABASE
# =========================================

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT
)
""")

conn.commit()

# =========================================
# ЭМОДЗИ
# =========================================

emojis = {
    "earn": "⭐",
    "tasks": "🎉",
    "withdraw": "🎁",
    "coupon": "✨",
    "bonus": "💎"
}

for key, value in emojis.items():

    exists = cur.execute(
        "SELECT value FROM settings WHERE key = ?",
        (key,)
    ).fetchone()

    if not exists:

        cur.execute(
            "INSERT INTO settings VALUES (?, ?)",
            (key, value)
        )

conn.commit()

# =========================================
# ПОЛУЧЕНИЕ ЭМОДЗИ
# =========================================

def get_emoji(name):

    emoji = cur.execute(
        "SELECT value FROM settings WHERE key = ?",
        (name,)
    ).fetchone()

    return emoji[0]

# =========================================
# ГЛАВНОЕ МЕНЮ
# =========================================

def get_menu():

    return ReplyKeyboardMarkup(
        keyboard=[

            [
                KeyboardButton(
                    text=f"{get_emoji('earn')} Заработать звёзды"
                ),

                KeyboardButton(
                    text=f"{get_emoji('tasks')} Задания"
                )
            ],

            [
                KeyboardButton(
                    text=f"{get_emoji('withdraw')} Вывести звёзды"
                )
            ],

            [
                KeyboardButton(
                    text=f"{get_emoji('coupon')} Активировать купон"
                )
            ],

            [
                KeyboardButton(
                    text=f"{get_emoji('bonus')} Бонус"
                )
            ]

        ],

        resize_keyboard=True
    )

# =========================================
# АДМИН МЕНЮ
# =========================================

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="🎨 Сменить эмоции"
            )
        ]
    ],
    resize_keyboard=True
)

# =========================================
# МЕНЮ СМЕНЫ ЭМОДЗИ
# =========================================

emoji_menu = ReplyKeyboardMarkup(
    keyboard=[

        [
            KeyboardButton(
                text="⭐ Заработок"
            ),

            KeyboardButton(
                text="🎉 Задания"
            )
        ],

        [
            KeyboardButton(
                text="🎁 Вывод"
            ),

            KeyboardButton(
                text="✨ Купон"
            )
        ],

        [
            KeyboardButton(
                text="💎 Бонус"
            )
        ]

    ],

    resize_keyboard=True
)

# =========================================
# СОСТОЯНИЯ
# =========================================

waiting_for = {}

# =========================================
# START
# =========================================

@dp.message(CommandStart())
async def start(message: Message):

    await message.answer(
        "⭐ Добро пожаловать!",
        reply_markup=get_menu()
    )

# =========================================
# АДМИН ПАНЕЛЬ
# =========================================

@dp.message(F.text == "/admins")
async def admins(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "⚙️ Админ панель",
        reply_markup=admin_menu
    )

# =========================================
# СМЕНА ЭМОДЗИ
# =========================================

@dp.message(F.text == "🎨 Сменить эмоции")
async def change_emoji(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "🎨 Выберите кнопку",
        reply_markup=emoji_menu
    )

# =========================================
# ВЫБОР КНОПКИ
# =========================================

@dp.message(F.text == "⭐ Заработок")
async def earn_emoji(message: Message):

    waiting_for[message.from_user.id] = "earn"

    await message.answer(
        "✍️ Отправьте новый эмодзи"
    )

@dp.message(F.text == "🎉 Задания")
async def tasks_emoji(message: Message):

    waiting_for[message.from_user.id] = "tasks"

    await message.answer(
        "✍️ Отправьте новый эмодзи"
    )

@dp.message(F.text == "🎁 Вывод")
async def withdraw_emoji(message: Message):

    waiting_for[message.from_user.id] = "withdraw"

    await message.answer(
        "✍️ Отправьте новый эмодзи"
    )

@dp.message(F.text == "✨ Купон")
async def coupon_emoji(message: Message):

    waiting_for[message.from_user.id] = "coupon"

    await message.answer(
        "✍️ Отправьте новый эмодзи"
    )

@dp.message(F.text == "💎 Бонус")
async def bonus_emoji(message: Message):

    waiting_for[message.from_user.id] = "bonus"

    await message.answer(
        "✍️ Отправьте новый эмодзи"
    )

# =========================================
# СОХРАНЕНИЕ ЭМОДЗИ
# =========================================

@dp.message()
async def save_emoji(message: Message):

    user_id = message.from_user.id

    if user_id not in waiting_for:
        return

    key = waiting_for[user_id]

    new_emoji = message.text

    cur.execute(
        "UPDATE settings SET value = ? WHERE key = ?",
        (new_emoji, key)
    )

    conn.commit()

    del waiting_for[user_id]

    await message.answer(
        "✅ Эмодзи изменён",
        reply_markup=get_menu()
    )

# =========================================
# ЗАПУСК
# =========================================

async def main():

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
