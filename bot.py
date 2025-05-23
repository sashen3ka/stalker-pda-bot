import asyncio
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import CallbackQuery

from ai.advice import generate_advice_from_state

from handlers.questions import (
    ask_energy,
    ask_fatigue,
    ask_motivation,
    ask_psi_noise,
    ask_sleep,
    ask_socio_signal,
    ask_inner_voice,
    ask_cipher,
)
from handlers.responses import (
    process_energy,
    process_fatigue,
    process_motivation,
    process_psi_noise,
    process_sleep,
    process_socio,
    process_inner_voice,
)
from handlers.cipher import process_cipher
from handlers.start import cmd_start, handle_start_scan

from utils.state import user_state
from utils.state_map import energy_map, fatigue_map, motivation_map, psi_map, sleep_map, social_map, voice_map




# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Инициализация OpenRouter бота
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(F.text == "/start")
async def start_cmd(message: types.Message):
    await cmd_start(message)

@dp.callback_query(F.data == "start_scan")
async def start_scan(callback: CallbackQuery):
    await handle_start_scan(callback)


# Обработчики ответов пользователя
@dp.callback_query(F.data.startswith("energy_"))
async def handle_energy(callback: types.CallbackQuery):
    await process_energy(callback)


@dp.callback_query(F.data.startswith("fatigue_"))
async def handle_fatigue(callback: types.CallbackQuery):
    await process_fatigue(callback)


@dp.callback_query(F.data.startswith("motivation_"))
async def handle_motivation(callback: types.CallbackQuery):
    await process_motivation(callback)


@dp.callback_query(F.data.startswith("psi_"))
async def handle_psi(callback: types.CallbackQuery):
    await process_psi_noise(callback)


@dp.callback_query(F.data.startswith("sleep_"))
async def handle_sleep(callback: types.CallbackQuery):
    await process_sleep(callback)


@dp.callback_query(F.data.startswith("socio_"))
async def handle_socio(callback: types.CallbackQuery):
    await process_socio(callback)


@dp.callback_query(F.data.startswith("voice_"))
async def handle_inner_voice(callback: types.CallbackQuery):
    await process_inner_voice(callback)
    
    
@dp.callback_query(F.data == "repeat_advice")
async def repeat_advice(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    state_raw = user_state.get(user_id, {}).get("current", {})
    
    # 🧽 Удаляем кнопку
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass

    if "cipher" not in state_raw:
        await callback.message.answer("⚠️ ПДА не видит Шифра дня. Пройди сканирование заново.")
        await callback.answer()
        return

    state = {
        "energy_text": energy_map.get(state_raw.get("energy")) or "—",
        "fatigue_text": fatigue_map.get(state_raw.get("fatigue")) or "—",
        "motivation_text": motivation_map.get(state_raw.get("motivation")) or "—",
        "psi_text": psi_map.get(state_raw.get("psi_noise")) or "—",
        "sleep_text": sleep_map.get(state_raw.get("sleep")) or "—",
        "social_text": social_map.get(state_raw.get("socio")) or "—",
        "inner_voice_text": voice_map.get(state_raw.get("inner_voice")) or "—",
        "cipher": state_raw.get("cipher", "—"),
    }

    await callback.message.answer("🔄 Переоценка состояния…")
    await generate_advice_from_state(callback.message, state, user_state)
    await callback.answer()



# Обработка финального текстового сообщения (шифра дня)
@dp.message()
async def handle_cipher(message: types.Message):
    await process_cipher(message)


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
