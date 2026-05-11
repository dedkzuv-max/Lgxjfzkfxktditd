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
friend_username = {}
wait_check = {}
user_amounts = {}
buy_type = {}
calc_users = {}
waiting_for_amount = {}

order_id = 100
orders = {}

# =========================
# КАЛЬКУЛЯТОР
# =========================

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
    user_id = message.from_user.id
    calc_users.pop(user_id, None)
    waiting_for_amount.pop(user_id, None)
    buy_type.pop(user_id, None)
    friend_username.pop(user_id, None)
    
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
# ФУНКЦИЯ ПОЛУЧЕНИЯ ИМЕНИ ПОЛЬЗОВАТЕЛЯ
# =========================

def get_user_display(user):
    """Возвращает красивое отображение пользователя"""
    if user.username:
        return f"@{user.username}"
    elif user.full_name:
        return user.full_name
    else:
        return f"Пользователь {user.id}"

# =========================
# КУПИТЬ
# =========================

@dp.callback_query(F.data == "buy")
async def buy(callback: CallbackQuery):
    user_id = callback.from_user.id
    waiting_for_amount.pop(user_id, None)
    buy_type.pop(user_id, None)
    friend_username.pop(user_id, None)
    user_amounts.pop(user_id, None)
    
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
    user_id = callback.from_user.id
    calc_users.pop(user_id, None)
    waiting_for_amount.pop(user_id, None)
    buy_type.pop(user_id, None)
    friend_username.pop(user_id, None)
    user_amounts.pop(user_id, None)
    wait_check.pop(user_id, None)

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
# КАЛЬКУЛЯТОР
# =========================

@dp.callback_query(F.data == "calc")
async def calc(callback: CallbackQuery):
    user_id = callback.from_user.id
    waiting_for_amount.pop(user_id, None)
    buy_type.pop(user_id, None)
    friend_username.pop(user_id, None)
    
    calc_users[user_id] = True

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
    user_id = callback.from_user.id
    waiting_for_amount.pop(user_id, None)
    friend_username.pop(user_id, None)
    user_amounts.pop(user_id, None)
    
    buy_type[user_id] = "self"
    waiting_for_amount[user_id] = True

    await callback.message.delete()
    await callback.message.answer(
        "💸 Сколько звезд хотите приобрести? (мин. 50)"
    )
    await callback.answer()

# =========================
# ДРУГУ
# =========================

@dp.callback_query(F.data == "friend_buy")
async def friend_buy(callback: CallbackQuery):
    user_id = callback.from_user.id
    waiting_for_amount.pop(user_id, None)
    user_amounts.pop(user_id, None)
    
    buy_type[user_id] = "friend"
    friend_username[user_id] = None

    await callback.message.delete()
    await callback.message.answer(
        "👤 Введите @username друга"
    )
    await callback.answer()

# =========================
# ОПЛАТА
# =========================

@dp.callback_query(F.data == "pay_kaspi")
async def pay_kaspi(callback: CallbackQuery):
    user_id = callback.from_user.id
    
    if user_id not in user_amounts:
        await callback.message.answer("❌ Ошибка. Попробуйте заново.")
        await callback.answer()
        return

    wait_check[user_id] = True
    amount = user_amounts[user_id]
    price = amount * RATE

    await callback.message.answer(
        f"""💳 К оплате: {price} KZT

Оплатите на Kaspi без комментариев:
{KASPI_TEXT}

После оплаты отправьте чек."""
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
        "⚙️ Админ панель",
        reply_markup=admin_menu
    )

# =========================
# КУРС
# =========================

@dp.callback_query(F.data == "admin_rate")
async def admin_rate(callback: CallbackQuery):
    admin_mode[callback.from_user.id] = "rate"
    await callback.message.answer("Введите новый курс:")
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
    await callback.message.answer("Введите новые реквизиты Kaspi:")
    await callback.answer()

# =========================
# ЧЕК
# =========================

@dp.message(F.photo | F.document)
async def check_handler(message: Message):
    global order_id

    user_id = message.from_user.id

    if user_id not in wait_check:
        return

    if user_id not in user_amounts:
        await message.answer("❌ Ошибка. Попробуйте заново.")
        wait_check.pop(user_id, None)
        return

    amount = user_amounts[user_id]
    price = amount * RATE

    # Красивое отображение покупателя
    buyer_display = get_user_display(message.from_user)

    # Определяем получателя
    if buy_type.get(user_id) == "friend":
        receiver_raw = friend_username.get(user_id, "не указан")
        # Если receiver_raw начинается с @, показываем как есть, иначе добавляем @
        if receiver_raw and not receiver_raw.startswith("@"):
            receiver_display = f"@{receiver_raw}"
        else:
            receiver_display = receiver_raw or "не указан"
    else:
        receiver_display = buyer_display

    order_id += 1
    orders[order_id] = user_id

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
        f"👤 От: {buyer_display}\n"
        f"📍 Кому: {receiver_display}\n"
        f"⭐ Количество: {amount}\n"
        f"💰 Сумма: {price} KZT"
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

    await message.answer("🪵 Чек принят, ожидайте подтверждения администратора!")

    # Очищаем состояния
    wait_check.pop(user_id, None)
    waiting_for_amount.pop(user_id, None)
    user_amounts.pop(user_id, None)
    friend_username.pop(user_id, None)
    buy_type.pop(user_id, None)

# =========================
# ВЫДАТЬ
# =========================

@dp.callback_query(F.data.startswith("accept_"))
async def accept_order(callback: CallbackQuery):
    order = int(callback.data.split("_")[1])
    user_id = orders[order]

    await bot.send_message(
        user_id,
        "✅ Заказ подтвержден, звезды будут отправлены в течение нескольких минут!"
    )
    await callback.message.edit_reply_markup(reply_markup=None)
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
        "❌ Заказ отклонен.\n\nПо вопросам: @Kuki_Star_Kz"
    )
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()

# =========================
# РЕФЕРАЛЫ
# =========================

@dp.callback_query(F.data == "refs")
async def refs(callback: CallbackQuery):
    await callback.message.answer(
        "🌿 Реферальная система скоро будет доступна!"
    )
    await callback.answer()

# =========================
# СООБЩЕНИЯ
# =========================

@dp.message()
async def messages(message: Message):
    global RATE, KASPI_TEXT

    user_id = message.from_user.id

    # КАЛЬКУЛЯТОР
    if user_id in calc_users:
        if message.text and message.text.isdigit():
            amount = int(message.text)
            price = amount * RATE
            video = FSInputFile("video.mp4")
            await message.answer_video(
                video=video,
                caption=(
                    f"🧮 Стоимость {amount} ⭐\n\n"
                    f"🇰🇿 {price} KZT"
                ),
                reply_markup=calc_back
            )
            return
        else:
            await message.answer("❌ Введите число")
            return

    # ADMIN
    if user_id in admin_mode:
        mode = admin_mode[user_id]
        if mode == "rate":
            try:
                RATE = float(message.text)
                await message.answer(f"✅ Новый курс: {RATE}")
            except:
                await message.answer("❌ Введите число")
        elif mode == "kaspi":
            KASPI_TEXT = message.text
            await message.answer("✅ Kaspi обновлен")
        admin_mode.pop(user_id, None)
        return

    # USERNAME ДРУГА
    if user_id in buy_type and buy_type[user_id] == "friend" and friend_username.get(user_id) is None:
        if message.text and message.text.startswith("@"):
            friend_username[user_id] = message.text
            waiting_for_amount[user_id] = True
            await message.answer(
                "💸 Сколько звезд хотите приобрести? (мин. 50)"
            )
            return
        else:
            await message.answer("❌ Введите username в формате @username")
            return

    # ОЖИДАНИЕ КОЛИЧЕСТВА ЗВЕЗД
    if user_id in waiting_for_amount:
        if message.text and message.text.isdigit():
            amount = int(message.text)
            if amount < 50:
                await message.answer("⚠️ Минимум 50 ⭐")
                return
            
            user_amounts[user_id] = amount
            waiting_for_amount.pop(user_id, None)
            
            await message.answer(
                f"💳 Оплата {amount} ⭐",
                reply_markup=pay_menu
            )
            return
        else:
            await message.answer("❌ Введите число (минимум 50)")
            return

# =========================
# ЗАПУСК
# =========================

async def main():
    print("Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())