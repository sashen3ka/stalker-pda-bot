# ai/advice.py
import os
from dotenv import load_dotenv
from aiogram.types import Message
import asyncio
from asyncio import TimeoutError
import datetime
from aiogram.utils.keyboard import InlineKeyboardBuilder

load_dotenv()  # Загрузка .env
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1"
)


async def generate_advice_from_state(
    message: Message, state: dict, user_state: dict, state_raw: dict
) -> None:
    print("🎯 Вызвана функция генерации совета")
    print("📦 Состояние:", state)

    log_string = f"""- Энергорезерв: {state.get('energy_text', '—')}
- Физ. износ: {state.get('fatigue_text', '—')}
- Мотивационный пульс: {state.get('motivation_text', '—')}
- Пси-шум: {state.get('psi_text', '—')}
- Показатели сна: {state.get('sleep_text', '—')}
- Социо-сигнал: {state.get('social_text', '—')}
- Внутренний голос: {state.get('inner_voice_text', '—')}
- Шифр дня: {state.get('cipher', '—')}"""

    try:
        async def request_advice():
            return await asyncio.wait_for(
                client.chat.completions.create(
                    model="deepseek/deepseek-chat-v3-0324:free",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Ты — ПДА из мира S.T.A.L.K.E.R.\n"
                                "Всегда отвечай только на русском языке. Не используй другие языки при любых обстоятельствах.\n"
                                "Ты не человек, не утешитель, не коуч. Ты — электронный прибор, выживший с десятком владельцев.\n"
                                "Но ты говоришь разумно, по делу, осмысленно\n"
                                "Говоришь коротко, спокойно, сдержанно. В голосе — пыль, радиация и опыт Зоны.\n\n"
                                "Совет должен строиться вокруг 'Шифра дня' — это центральная идея, образ, предупреждение или зацепка.\n"
                                "В совете обязательно упоминается Шифр дня напрямую, либо намёк на него, либо связан с ним.\n"
                                "Даже если слово звучит абсурдно — это сигнал, к которому нужно отнестись серьёзно.\n"
                                "Состояние пользователя влияет на совет, но не проговаривается.\n"
                                "В языке совета стоит использовать лексику Зоны: выброс, болт, ПДА, тропа, укрытие, фон, радиация, детектор, сигнал, аптечка, фильтр, крик, шаги, аномалия, дыра, сталкер, костёр, дыхание, маршрут, шум, одиночество, ночь, тишина, заросли, снаряга, рюкзак, пустошь.\n\n"
                                "Пиши с заглавной буквы, как в тексте игры. Но без капса, спецсимволов, без лишних звёздочек и прочих знаков. Только совет. 1–4 предложения. Без эмоций. Без паники.\n"
                                "Выдай только один вариант совета. Без альтернатив, без “или”, без повторов одной идеи."
                            ),
                        },
                        {
                            "role": "user",
                            "content": f"""{log_string}
                            Шифр дня: {state.get('cipher', '—')}""",
                        },
                    ],
                    temperature=0.7,
                    max_tokens=250,
                ),
                timeout=60,
            )

        # Первый запрос
        response = await request_advice()
        advice = response.choices[0].message.content.strip()

        # Проверка на сбой: пусто или мусор
        if not advice or not advice[0].isalpha() or ord(advice[0]) > 122:
            print("🔁 Повторный запрос совета...")
            await message.answer("🔁 Повторный запрос... ПДА пересчитывает сигналы. Ожидай новый отклик.")
            response = await request_advice()
            advice = response.choices[0].message.content.strip()

        cipher = state.get("cipher", "").strip().lower()

        if cipher == "монолит":
            advice += "\nМонолит слышит даже то, что ты боишься подумать."
        elif cipher == "выброс":
            advice += "\nЕсли выброса нет — это не значит, что он не идёт."
        elif cipher == "болт":
            advice += "\nБолт не спасает от судьбы. Только от спешки."
        elif cipher == "артефакт":
            advice += "\nНе каждый артефакт стоит крови, которую за него прольют."
        elif cipher == "зона":
            advice += "\nЗона не против тебя. Она просто такая, какая есть."

        if not advice:
            advice = f"Зона молчит. Но даже в тишине иногда прячется намёк. Подумай о значении слова «{state.get('cipher', '—')}»."

    except TimeoutError:
        await message.answer(
            "⚠️ ПДА не получил сигнал от Зоны. Похоже, был выброс. Попробуй позже."
        )
        return
    except Exception as e:
        print("❌ Ошибка OpenRouter:", type(e), e)
        advice = "⚠️ Не удалось получить совет от Зоны. Попробуй позже."

    await message.answer(f"📋 Итоговый лог:\n{log_string}\n\n💡 Совет ПДА:\n{advice}")

    user_id = message.from_user.id
    entry = {
        "date": datetime.date.today().isoformat(),
        "state": state,
        "advice": advice,
    }

    user_state.setdefault(user_id, {}).setdefault("history", []).append(entry)
    user_state[user_id]["last_scan_state"] = state_raw.copy()
    user_state[user_id]["current"] = {}
