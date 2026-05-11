import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile
)

TOKEN = "8799385592:AAEsPJ6vMXx0P5Eq_iSqXcUlyCvvW0szJwA"
ADMIN_ID = 8656094320

bot = Bot(token=TOKEN)
dp = Dispatcher()

# =========================
# НАСТРОЙКИ
# =========================

RATE = 7.5
KASPI_TEXT = "4400430347936632"

admin_mode = {}
friend_users = {}
buy_users = {}
user_amounts = {}

order_id = 100
orders = {}

# =========================
# КАЛЬКУЛЯТОР
# =========================

calc_users = {}

calc_back = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="back_main"
            )
        ]
    ]
)

# =========================
# ГЛАВНОЕ МЕНЮ
# =========================

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

# =========================
# ПОКУПКА
# =========================

buy_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🙋 Себе",
                callback_data="self_buy"
            ),
            InlineKeyboardButton(
                text="🎁 Другу",
                callback_data="friend_buy"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="back_main"
            )
        ]
    ]
)

# =========================
# ОПЛАТА
# =========================

pay_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="💸 Kaspi",
                callback_data="pay_kaspi"
            )
        ]
    ]
)

# =========================
# АДМИН МЕНЮ
# =========================

admin_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="💸 Курс",
                callback_data="admin_rate"
            )
        ],
        [
            InlineKeyboardButton(
                text="💳 Реквизиты",
                callback_data="admin_reqs"
            )
        ]
    ]
)

# =========================
# РЕКВИЗИТЫ
# =========================

reqs_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="💳 Kaspi",
                callback_data="admin_kaspi"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="back_admin"
            )
        ]
    ]
)

# =========================
# START
# =========================

@dp.message(CommandStart())
async def start(message: Message):

    video = FSInputFile("video.mp4")

    await message.answer_video(
        video=video,
        caption=(
            "🌲👋 Добро пожаловать в Bro Stars!\n\n"
            "Самые дешевые звезды 💸\n"
            "Покупка от 50 ⭐"
        ),
        reply_markup=menu
    )

# =========================
# КУПИТЬ
# =========================

@dp.callback_query(F.data == "buy")
async def buy(callback: CallbackQuery):

    await callback.message.delete()

    video = FSInputFile("video.mp4")

    await callback.message.answer_video(
        video=video,
        caption="🌟 Покупка Stars\n\nДля кого покупаем?",
        reply_markup=buy_menu
    )

    await callback.answer()

# =========================
# НАЗАД
# =========================

@dp.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):

    await callback.message.delete()

    video = FSInputFile("video.mp4")

    await callback.message.answer_video(
        video=video,
        caption=(
            "🌲👋 Добро пожаловать в Bro Stars!\n\n"
            "Самые дешевые звезды 💸\n"
            "Покупка от 50 ⭐"
        ),
        reply_markup=menu
    )

    await callback.answer()

# =========================
# КАЛЬКУЛЯТОР ОТКРЫТЬ
# =========================

@dp.callback_query(F.data == "calc")
async def calc(callback: CallbackQuery):

    calc_users[callback.from_user.id] = True

    await callback.message.delete()

    video = FSInputFile("video.mp4")

    await callback.message.answer_video(
        video=video,
        caption="🧮 Калькулятор Stars\n\nВведите количество звезд:",
        reply_markup=calc_back
    )

    await callback.answer()

# =========================
# СЕБЕ
# =========================

@dp.callback_query(F.data == "self_buy")
async def self_buy(callback: CallbackQuery):

    buy_users[callback.from_user.id] = True

    await callback.message.answer(
        "Обязательно установите имя пользователя! 💸 Сколько звезд хотите приобрести(мин. 50)?"
    )

    await callback.answer()

# =========================
# ДРУГУ
# =========================

@dp.callback_query(F.data == "friend_buy")
async def friend_buy(callback: CallbackQuery):

    friend_users[callback.from_user.id] = True

    await callback.message.answer(
        "👤 Введите @username друга"
    )

    await callback.answer()

# =========================
# ОПЛАТА
# =========================

@dp.callback_query(F.data == "pay_kaspi")
async def pay_kaspi(callback: CallbackQuery):

    amount = user_amounts.get(callback.from_user.id, 0)
    price = amount * RATE

    await callback.message.answer(
        f"""💳 К оплате: {price} KZT

Оплатите на Kaspi без комментариев: {KASPI_TEXT}

Отправьте чек в течение 30 минут."""
    )

    await callback.answer()

# =========================
# АДМИНКА
# =========================

@dp.message(F.text == "/apanel")
async def admin_panel(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "ㅤ",
        reply_markup=admin_menu
    )

# =========================
# КУРС
# =========================

@dp.callback_query(F.data == "admin_rate")
async def admin_rate(callback: CallbackQuery):

    admin_mode[callback.from_user.id] = "rate"

    await callback.message.answer(
        "Введите курс:"
    )

    await callback.answer()

# =========================
# РЕКВИЗИТЫ
# =========================

@dp.callback_query(F.data == "admin_reqs")
async def admin_reqs(callback: CallbackQuery):

    await callback.message.edit_reply_markup(
        reply_markup=reqs_menu
    )

    await callback.answer()

# =========================
# НАЗАД АДМИНКА
# =========================

@dp.callback_query(F.data == "back_admin")
async def back_admin(callback: CallbackQuery):

    await callback.message.edit_reply_markup(
        reply_markup=admin_menu
    )

    await callback.answer()

# =========================
# KASPI
# =========================

@dp.callback_query(F.data == "admin_kaspi")
async def admin_kaspi(callback: CallbackQuery):

    admin_mode[callback.from_user.id] = "kaspi"

    await callback.message.answer(
        "Введите текст Kaspi:"
    )

    await callback.answer()

# =========================
# ЧЕК
# =========================

@dp.message(F.photo | F.document)
async def check_handler(message: Message):

    global order_id

    if message.from_user.id not in user_amounts:
        return

    amount = user_amounts[message.from_user.id]
    price = amount * RATE

    username = message.from_user.username

    if not username:
        username = "нет"

    order_id += 1

    orders[order_id] = message.from_user.id

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Выдать",
                    callback_data=f"accept_{order_id}"
                ),
                InlineKeyboardButton(
                    text="❌ Отклонить",
                    callback_data=f"decline_{order_id}"
                )
            ]
        ]
    )

    text = (
        f"🔔 ЗАКАЗ #{order_id}\n\n"
        f"👤 @{username}\n"
        f"⭐ {amount}\n"
        f"💳 {price} KZT"
    )

    if message.photo:

        await bot.send_photo(
            ADMIN_ID,
            photo=message.photo[-1].file_id,
            caption=text,
            reply_markup=keyboard
        )

    elif message.document:

        await bot.send_document(
            ADMIN_ID,
            document=message.document.file_id,
            caption=text,
            reply_markup=keyboard
        )

    await message.answer(
        "🪵 Чек принят, ожидайте подтверждения администратора!"
    )

# =========================
# ВЫДАТЬ
# =========================

@dp.callback_query(F.data.startswith("accept_"))
async def accept_order(callback: CallbackQuery):

    order = int(callback.data.split("_")[1])

    user_id = orders[order]

    await bot.send_message(
        user_id,
        "✅ Заказ подтвержден, звезды будут отправлены в течение нескольких минут, будем рады вашему отзыву @KukiStarkz !"
    )

    await callback.message.edit_reply_markup(
        reply_markup=None
    )

    await callback.answer()

# =========================
# ОТКЛОНИТЬ
# =========================

@dp.callback_query(F.data.startswith("decline_"))
async def decline_order(callback: CallbackQuery):

    order = int(callback.data.split("_")[1])

    user_id = orders[order]

    await bot.send_message(
        user_id,
        "❌ Заказ отклонен.\n\nПо вопросам вы можете обратиться в поддержку @Kuki_Star_Kz"
    )

    await callback.message.edit_reply_markup(
        reply_markup=None
    )

    await callback.answer()

# =========================
# СООБЩЕНИЯ + КАЛЬКУЛЯТОР
# =========================

@dp.message()
async def messages(message: Message):

    global RATE, KASPI_TEXT

    # =========================
    # КАЛЬКУЛЯТОР
    # =========================

    if message.from_user.id in calc_users:

        if message.text and message.text.isdigit():

            amount = int(message.text)
            price = amount * RATE

            video = FSInputFile("video.mp4")

            await message.answer_video(
                video=video,
                caption=f"🧮 Стоимость {amount} ⭐\n\n🇰🇿 {price} KZT",
                reply_markup=calc_back
            )

            calc_users.pop(message.from_user.id, None)
            return

    # =========================
    # ADMIN
    # =========================

    if message.from_user.id in admin_mode:

        mode = admin_mode[message.from_user.id]

        if mode == "rate":

            RATE = float(message.text)

            await message.answer(
                f"Новый курс: {RATE}"
            )

        elif mode == "kaspi":

            KASPI_TEXT = message.text

            await message.answer(
                "Kaspi обновлен."
            )

        del admin_mode[message.from_user.id]
        return

    # =========================
    # ДРУГ
    # =========================

    if message.from_user.id in friend_users:

        if message.text.startswith("@"):

            friend_users[message.from_user.id] = message.text

            await message.answer(
                f"Для {message.text}. Сколько звезд?"
            )

            return

    # =========================
    # ПОКУПКА
    # =========================

    if message.from_user.id in buy_users and message.text and message.text.isdigit():

        amount = int(message.text)

        if amount < 50:

            await message.answer("⚠️ Минимум 50.")

        else:

            user_amounts[message.from_user.id] = amount

            await message.answer(
                f"Оплата **{amount} ⭐**:",
                parse_mode="Markdown",
                reply_markup=pay_menu
            )

        buy_users.pop(message.from_user.id, None)

# =========================
# ЗАПУСК
# =========================

async def main():
    print("Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())