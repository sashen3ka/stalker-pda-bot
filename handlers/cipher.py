# handlers/cipher.py
from aiogram import types
from utils.state import user_state
from utils.state_map import (
    energy_map,
    fatigue_map,
    motivation_map,
    psi_map,
    sleep_map,
    social_map,
    voice_map,
)
from ai.advice import generate_advice_from_state


async def process_cipher(message: types.Message):
    user_id = message.from_user.id
    text = message.text.strip()

    state_raw = user_state.get(user_id, {}).get("current", {})
    if "inner_voice" in state_raw and "cipher" not in state_raw:
        state_raw["cipher"] = text
        user_state[user_id]["current"] = state_raw

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

        await message.answer(f"Шифр дня зафиксирован: <b>{text}</b>")
        await message.answer("ПДА: Сканирование завершено. Готовлю сводку и совет…")

        await generate_advice_from_state(message, state, user_state, state_raw)

