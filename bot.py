import asyncio
import time
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
broadcast_mode = {}

order_id = 100
orders = {}
order_data = {}

# =========================
# СТАТИСТИКА
# =========================
total_users = set()
total_stars_sold = 0
total_orders_completed = 0
total_revenue = 0

# =========================
# ЛОГИ ЗАЯВОК
# =========================
order_logs = []

def add_order_log(order_num, user_id, buyer_name, receiver_name, amount, price, status, admin_name):
    order_logs.append({
        "order_id": order_num,
        "user_id": user_id,
        "buyer": buyer_name,
        "receiver": receiver_name,
        "amount": amount,
        "price": price,
        "status": status,
        "admin": admin_name,
        "time": time.time()
    })

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
                url="https://t.me/KukiStarkz"
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
            ),
            InlineKeyboardButton(
                text="💳 Реквизиты",
                callback_data="admin_reqs"
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Статистика",
                callback_data="admin_stats"
            ),
            InlineKeyboardButton(
                text="📢 Рассылка",
                callback_data="admin_broadcast"
            )
        ],
        [
            InlineKeyboardButton(
                text="📋 Логи заявок",
                callback_data="admin_logs"
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
    total_users.add(user_id)
    
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
# СТАТИСТИКА
# =========================

@dp.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Доступ запрещен")
        return
    
    stats_text = (
        f"📊 СТАТИСТИКА БОТА\n\n"
        f"👥 Пользователей: {len(total_users)}\n"
        f"⭐ Продано звезд: {total_stars_sold}\n"
        f"💰 Выручка: {total_revenue} KZT\n"
        f"✅ Выполнено заказов: {total_orders_completed}\n"
        f"📋 Всего заявок в логах: {len(order_logs)}"
    )
    
    await callback.message.answer(stats_text)
    await callback.answer()

# =========================
# РАССЫЛКА
# =========================

@dp.callback_query(F.data == "admin_broadcast")
async def admin_broadcast(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Доступ запрещен")
        return
    
    broadcast_mode[callback.from_user.id] = True
    await callback.message.answer(
        "📢 Введите текст для рассылки всем пользователям:\n\n"
        "Отправьте текст, фото или видео для рассылки."
    )
    await callback.answer()

# =========================
# ЛОГИ ЗАЯВОК
# =========================

@dp.callback_query(F.data == "admin_logs")
async def admin_logs(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Доступ запрещен")
        return
    
    if not order_logs:
        await callback.message.answer("📋 Логов пока нет")
        await callback.answer()
        return
    
    logs_text = "📋 ПОСЛЕДНИЕ ЗАЯВКИ:\n\n"
    for log in order_logs[-10:]:
        status_emoji = "✅" if log["status"] == "принят" else "❌"
        logs_text += (
            f"{status_emoji} #{log['order_id']} | {log['status']}\n"
            f"   👤 {log['buyer']} → {log['receiver']}\n"
            f"   ⭐ {log['amount']} | {log['price']} KZT\n"
            f"   👨‍💼 {log['admin']}\n\n"
        )
    
    full_log_btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📋 Полный лог", callback_data="admin_full_log")]
        ]
    )
    
    await callback.message.answer(logs_text, reply_markup=full_log_btn)
    await callback.answer()

@dp.callback_query(F.data == "admin_full_log")
async def admin_full_log(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Доступ запрещен")
        return
    
    if not order_logs:
        await callback.message.answer("📋 Логов пока нет")
        await callback.answer()
        return
    
    full_text = "📋 ПОЛНЫЙ ЛОГ ЗАЯВОК:\n\n"
    for log in order_logs:
        status_emoji = "✅" if log["status"] == "принят" else "❌"
        full_text += f"{status_emoji} #{log['order_id']} | {log['status']} | {log['amount']}⭐ | {log['price']}KZT | {log['admin']}\n"
    
    if len(full_text) > 4000:
        short_text = "📋 ПОСЛЕДНИЕ 50 ЗАЯВОК:\n\n"
        for log in order_logs[-50:]:
            status_emoji = "✅" if log["status"] == "принят" else "❌"
            short_text += f"{status_emoji} #{log['order_id']} | {log['status']} | {log['amount']}⭐ | {log['price']}KZT\n"
        await callback.message.answer(short_text)
    else:
        await callback.message.answer(full_text)
    
    await callback.answer()

# =========================
# КУРС
# =========================

@dp.callback_query(F.data == "admin_rate")
async def admin_rate(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Доступ запрещен")
        return
    admin_mode[callback.from_user.id] = "rate"
    await callback.message.answer("Введите новый курс:")
    await callback.answer()

# =========================
# РЕКВИЗИТЫ
# =========================

@dp.callback_query(F.data == "admin_reqs")
async def admin_reqs(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Доступ запрещен")
        return
    await callback.message.edit_reply_markup(
        reply_markup=reqs_menu
    )
    await callback.answer()

# =========================
# НАЗАД АДМИНКА
# =========================

@dp.callback_query(F.data == "back_admin")
async def back_admin(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Доступ запрещен")
        return
    await callback.message.edit_reply_markup(
        reply_markup=admin_menu
    )
    await callback.answer()

# =========================
# KASPI
# =========================

@dp.callback_query(F.data == "admin_kaspi")
async def admin_kaspi(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Доступ запрещен")
        return
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

    buyer_display = get_user_display(message.from_user)

    if buy_type.get(user_id) == "friend":
        receiver_raw = friend_username.get(user_id, "не указан")
        if receiver_raw and not receiver_raw.startswith("@"):
            receiver_display = f"@{receiver_raw}"
        else:
            receiver_display = receiver_raw or "не указан"
    else:
        receiver_display = buyer_display

    order_id += 1
    orders[order_id] = user_id
    
    order_data[order_id] = {
        "amount": amount,
        "price": price,
        "buyer": buyer_display,
        "receiver": receiver_display
    }

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
    global total_stars_sold, total_orders_completed, total_revenue
    
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Доступ запрещен")
        return
    
    order = int(callback.data.split("_")[1])
    user_id = orders[order]
    
    order_info = order_data.get(order, {})
    amount = order_info.get("amount", 0)
    price = order_info.get("price", 0)
    buyer_name = order_info.get("buyer", "неизвестно")
    receiver_name = order_info.get("receiver", "неизвестно")
    
    total_stars_sold += amount
    total_revenue += price
    total_orders_completed += 1

    await bot.send_message(
        user_id,
        "✅ Заказ подтвержден, звезды будут отправлены в течение нескольких минут, будем рады вашему отзыву @KukiStarkz !"
    )
    await callback.message.edit_reply_markup(reply_markup=None)
    
    add_order_log(order, user_id, buyer_name, receiver_name, amount, price, "принят", callback.from_user.username or "админ")
    
    await callback.answer(f"✅ Заказ #{order} принят! +{amount}⭐, {price}KZT")

# =========================
# ОТКЛОНИТЬ
# =========================

@dp.callback_query(F.data.startswith("decline_"))
async def decline_order(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Доступ запрещен")
        return
    
    order = int(callback.data.split("_")[1])
    user_id = orders[order]
    
    order_info = order_data.get(order, {})
    amount = order_info.get("amount", 0)
    price = order_info.get("price", 0)
    buyer_name = order_info.get("buyer", "неизвестно")
    receiver_name = order_info.get("receiver", "неизвестно")

    await bot.send_message(
        user_id,
        "❌ Заказ отклонен.По вопросамвы можетеобратитьсяв поддержку @Kuki_Star_Kz"
    )
    await callback.message.edit_reply_markup(reply_markup=None)
    
    add_order_log(order, user_id, buyer_name, receiver_name, amount, price, "отклонен", callback.from_user.username or "админ")
    
    await callback.answer(f"❌ Заказ #{order} отклонен!")

# =========================
# РАССЫЛКА (ОБРАБОТЧИК)
# =========================

@dp.message()
async def messages(message: Message):
    global RATE, KASPI_TEXT

    user_id = message.from_user.id

    if user_id in broadcast_mode:
        if message.from_user.id != ADMIN_ID:
            broadcast_mode.pop(user_id, None)
            return
        
        success_count = 0
        fail_count = 0
        
        await message.answer("📢 Начинаю рассылку...")
        
        for uid in total_users:
            try:
                if message.text:
                    await bot.send_message(uid, message.text)
                elif message.photo:
                    await bot.send_photo(uid, message.photo[-1].file_id, caption=message.caption)
                elif message.video:
                    await bot.send_video(uid, message.video.file_id, caption=message.caption)
                success_count += 1
            except:
                fail_count += 1
        
        await message.answer(
            f"📢 Рассылка завершена!\n\n"
            f"✅ Доставлено: {success_count}\n"
            f"❌ Не доставлено: {fail_count}"
        )
        
        broadcast_mode.pop(user_id, None)
        return

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
# РЕФЕРАЛЫ
# =========================

@dp.callback_query(F.data == "refs")
async def refs(callback: CallbackQuery):
    await callback.message.answer(
        "🌿 Реферальная система скоро будет доступна!"
    )
    await callback.answer()

# =========================
# ЗАПУСК
# =========================

async def main():
    print("Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())