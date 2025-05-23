# handlers/start.py
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery
from handlers.questions import ask_energy
import datetime
from utils.state import user_state

DEBUG_MODE = True  # 🔧 Установи в False для включения ограничения


async def handle_start_scan(callback: CallbackQuery):
    # Удаляем сообщение с кнопкой
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    user_id = callback.from_user.id
    today = datetime.date.today()

    user_data = user_state.get(user_id, {})
    last_scan = user_data.get("last_scan")

    if not DEBUG_MODE and last_scan == today:
        await callback.message.answer("🛑 ПДА уже сканировал тебя сегодня.\nВернись завтра, сталкер.")
        await callback.answer()
        return

    user_state[user_id] = {
        "last_scan": today,
        "current": {},
        "history": user_data.get("history", [])
    }

    await ask_energy(callback)
    await callback.answer()




async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="🧠 Начать сканирование", callback_data="start_scan")
    await message.answer("📡 ПДА выходит на частоту...\nГотов к сканированию, сталкер.", reply_markup=builder.as_markup())
