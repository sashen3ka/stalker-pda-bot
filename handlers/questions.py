# handlers/questions.py
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
import random
from utils.state import user_state


async def ask_energy(callback: types.CallbackQuery):
    prompts = [
        "ПДА: Сколько осталось сил после вылазки?",
        "ПДА: Энергия на нуле или ещё держишься?",
        "ПДА: Проверка батарей. Уровень заряда?",
        "ПДА: Насколько ты боеспособен, сталкер?",
        "ПДА: Оцени свой заряд. Ты на пределе или в норме?",
        "ПДА: Сколько осталось энергии в твоём аккумуляторе?",
        "ПДА: Как у тебя с запасом сил сегодня?",
    ]

    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="💀 На пределе", callback_data="energy_1"),
        types.InlineKeyboardButton(text="⏳ Запас тает", callback_data="energy_2"),
    )
    builder.row(
        types.InlineKeyboardButton(text="🛡️ Боеспособен", callback_data="energy_3"),
        types.InlineKeyboardButton(text="✅ Полный заряд", callback_data="energy_4"),
    )

    user_id = callback.from_user.id
    old_msg_id = user_state.get(user_id, {}).get("last_message_id")
    if old_msg_id:
        try:
            await callback.bot.delete_message(callback.message.chat.id, old_msg_id)
        except:
            pass

    msg = await callback.message.answer(random.choice(prompts), reply_markup=builder.as_markup())
    user_state.setdefault(user_id, {})["last_message_id"] = msg.message_id


async def ask_fatigue(callback: types.CallbackQuery):
    prompts = [
        "ПДА: Как себя чувствует тело?",
        "ПДА: Износ чувствуется?",
        "ПДА: Есть ли усталость в суставах и мышцах?",
        "ПДА: Как ощущения после последней вылазки?",
        "ПДА: Тело бодро или слабеет?",
        "ПДА: Каковы последствия последней вылазки на организм?",
        "ПДА: Остатки сил — на пределе или с запасом?",
        "ПДА: Тело наготове или подводит?",
        "ПДА: Оцените текущий статус биосистемы.",
        "ПДА: Обнаружен ли износ опорно-двигательного аппарата?",
        "ПДА: Зафиксированы ли повреждения в мышечной ткани?",
        "ПДА: Отчёт по подвижности суставов: в норме или ограничена?",
        "ПДА: Текущий энергетический баланс тела: стабильный или сниженный?",
        "ПДА: Состояние моторики и координации, подтвердите."
    ]
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🔥 Пульс в норме, энергия в крови", callback_data="fatigue_1"))
    builder.row(types.InlineKeyboardButton(text="🤕 Слегка устал, но впереди дорога", callback_data="fatigue_2"))
    builder.row(types.InlineKeyboardButton(text="🧱 Песок в суставах", callback_data="fatigue_3"))

    user_id = callback.from_user.id
    old_msg_id = user_state.get(user_id, {}).get("last_message_id")
    if old_msg_id:
        try:
            await callback.bot.delete_message(callback.message.chat.id, old_msg_id)
        except:
            pass

    msg = await callback.message.answer(random.choice(prompts), reply_markup=builder.as_markup())
    user_state.setdefault(user_id, {})["last_message_id"] = msg.message_id


async def ask_motivation(callback: types.CallbackQuery):
    prompts = [
        "ПДА: Хочется ли сегодня что-то делать, сталкер?",
        "ПДА: Есть ли у тебя импульс двигаться вперёд?",
        "ПДА: Что там с мотивацией? Или двигаешься по инерции?",
        "ПДА: Насколько ты в боевом духе сегодня?",
        "ПДА: Огонь внутри — горит или угасает?",
        "ПДА: Есть ли желание идти вперёд и искать артефакты?",
        "ПДА: Статус боевого духа: стабилен или снижен?",
        "ПДА: Мотивационная цепь активна?",
        "ПДА: Уровень стремления к выполнению задач?",
        "ПДА: Целеполагание активно?",
        "ПДА: Мотивационный модуль в рабочем режиме?"
    ]
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🦾 Рвусь в бой", callback_data="motivation_1"))
    builder.row(types.InlineKeyboardButton(text="🔄 Двигаюсь по инерции", callback_data="motivation_2"))
    builder.row(types.InlineKeyboardButton(text="💀 Хоть бы спрятаться", callback_data="motivation_3"))

    user_id = callback.from_user.id
    old_msg_id = user_state.get(user_id, {}).get("last_message_id")
    if old_msg_id:
        try:
            await callback.bot.delete_message(callback.message.chat.id, old_msg_id)
        except:
            pass

    msg = await callback.message.answer(random.choice(prompts), reply_markup=builder.as_markup())
    user_state.setdefault(user_id, {})["last_message_id"] = msg.message_id


async def ask_psi_noise(callback: types.CallbackQuery):
    prompts = [
        "ПДА: Мешают ли внутренние помехи?",
        "ПДА: Шумит ли внутри?",
        "ПДА: В голове порядок или пси-гул?",
        "ПДА: Пси-активность мешает твоей работе?",
        "ПДА: Чувствуешь ли пси-шум или шторм?",
        "ПДА: Обнаружены ли пси-флуктуации?",
        "ПДА: Проверка пси-поля: стабильность сохранена?",
        "ПДА: Внутренний шум зарегистрирован?",
        "ПДА: Оценка пси-среды: чисто или возмущено?",
        "ПДА: Зафиксированы ли аномальные колебания сознания?",
        "ПДА: Состояние ментального фона?",
        "ПДА: Анализ нейрополя: фон, гул или шторм?"
    ]
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🧘 Чисто", callback_data="psi_1"))
    builder.row(types.InlineKeyboardButton(text="🌫️ Фоновый гул", callback_data="psi_2"))
    builder.row(types.InlineKeyboardButton(text="🌩️ Пси-шторм", callback_data="psi_3"))

    user_id = callback.from_user.id
    old_msg_id = user_state.get(user_id, {}).get("last_message_id")
    if old_msg_id:
        try:
            await callback.bot.delete_message(callback.message.chat.id, old_msg_id)
        except:
            pass

    msg = await callback.message.answer(random.choice(prompts), reply_markup=builder.as_markup())
    user_state.setdefault(user_id, {})["last_message_id"] = msg.message_id


async def ask_sleep(callback: types.CallbackQuery):
    prompts = [
        "ПДА: Что творилось ночью?",
        "ПДА: Сон был крепким или Зона шептала?",
        "ПДА: Выспался или блуждал по коридорам сна?",
        "ПДА: Как прошла ночь? Спал спокойно?",
        "ПДА: Были ли тревожные сны или просыпания?",
        "ПДА: Оценка качества сна за последнюю ночь?",
        "ПДА: Зафиксирован ли восстановительный цикл в ночной фазе?",
        "ПДА: Состояние сна: стабильное или нарушенное?",
        "ПДА: Была ли ночь использована для регенерации?",
        "ПДА: Качество сна соответствует нормативу?",
        "ПДА: Обнаружены ли прерывания фазы отдыха?",
        "ПДА: Зафиксирована ли полная перезагрузка сознания?",
        "ПДА: Режим сна — активен, фрагментирован или отсутствует?",
        "ПДА: Период ночного восстановления завершён успешно?",
        "ПДА: Уровень глубины сна достаточен?",
        "ПДА: Восстановление через сон выполнено?"
    ]
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🛌 Ночь прошла без шороха", callback_data="sleep_1"))
    builder.row(types.InlineKeyboardButton(text="⏰ Сон с перебоями", callback_data="sleep_2"))
    builder.row(types.InlineKeyboardButton(text="👁️ Сон тревожный", callback_data="sleep_3"))
    builder.row(types.InlineKeyboardButton(text="🌑 Не спал", callback_data="sleep_4"))

    user_id = callback.from_user.id
    old_msg_id = user_state.get(user_id, {}).get("last_message_id")
    if old_msg_id:
        try:
            await callback.bot.delete_message(callback.message.chat.id, old_msg_id)
        except:
            pass

    msg = await callback.message.answer(random.choice(prompts), reply_markup=builder.as_markup())
    user_state.setdefault(user_id, {})["last_message_id"] = msg.message_id


async def ask_socio_signal(callback: types.CallbackQuery):
    prompts = [
        "ПДА: Как с другими сталкерами?",
        "ПДА: В эфире один или ловишь отклики?",
        "ПДА: Сигнал от мира принимается или глушишь?",
        "ПДА: Уровень социального контакта соответствует норме?",
        "ПДА: Насколько ты открыт для контактов?",
        "ПДА: Как обстоят дела с коммуникацией?",
        "ПДА: Готовность к взаимодействию с другими подтверждена?",
        "ПДА: Статус коммуникативной системы: открыт, ограничен, перегружен?",
        "ПДА: Фиксация уровня социальной доступности...",
        "ПДА: Протокол связи с внешним окружением активирован?",
        "ПДА: Оценка текущего социо-сигнала",
        "ПДА: Взаимодействие с группой — в норме или снижено?",
        "ПДА: Коммуникационные цепи активны или прерваны?",
        "ПДА: Обнаружены признаки социальной перегрузки?"
    ]
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🔒 Изоляция — мой выбор", callback_data="socio_1"))
    builder.row(types.InlineKeyboardButton(text="📡 Приём стабилен", callback_data="socio_2"))
    builder.row(types.InlineKeyboardButton(text="🆘 Если кто на связи — отзовись", callback_data="socio_3"))
    builder.row(types.InlineKeyboardButton(text="⚠️ Перегруз от людей", callback_data="socio_4"))

    user_id = callback.from_user.id
    old_msg_id = user_state.get(user_id, {}).get("last_message_id")
    if old_msg_id:
        try:
            await callback.bot.delete_message(callback.message.chat.id, old_msg_id)
        except:
            pass

    msg = await callback.message.answer(random.choice(prompts), reply_markup=builder.as_markup())
    user_state.setdefault(user_id, {})["last_message_id"] = msg.message_id


async def ask_inner_voice(callback: types.CallbackQuery):
    prompts = [
        "ПДА: Что шепчет тебе Зона внутри?",
        "ПДА: Какой голос звучит в голове?",
        "ПДА: Внутренний голос — друг или враг?",
        "ПДА: Чего тебе подсказывает внутренний голос?",
        "ПДА: Поддержка или критика — что слышишь?",
        "ПДА: Что говорит тебе твоя совесть и разум?",
        "ПДА: Внутренний приёмник — на поддержке, в молчании или в сбое?",
        "ПДА: Внутренний голос активен? Что слышишь?",
        "ПДА: Состояние внутреннего эфира: сигнал принят?",
        "ПДА: Что тебе шепчет Зона внутри?",
        "ПДА: Голос внутри молчит, помогает или мешает?",
        "ПДА: Что говорит тебе Зона внутри?",
        "ПДА: Зона говорит с каждым. Что говорит с тобой?"
    ]
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🛡️ Поддерживает", callback_data="voice_1"))
    builder.row(types.InlineKeyboardButton(text="🕳️ Молчит", callback_data="voice_2"))
    builder.row(types.InlineKeyboardButton(text="🗡️ Критикует", callback_data="voice_3"))
    builder.row(types.InlineKeyboardButton(text="🤡 Высмеивает", callback_data="voice_4"))

    user_id = callback.from_user.id
    old_msg_id = user_state.get(user_id, {}).get("last_message_id")
    if old_msg_id:
        try:
            await callback.bot.delete_message(callback.message.chat.id, old_msg_id)
        except:
            pass

    msg = await callback.message.answer(random.choice(prompts), reply_markup=builder.as_markup())
    user_state.setdefault(user_id, {})["last_message_id"] = msg.message_id


async def ask_cipher(callback: types.CallbackQuery):
    prompts = [
        "ПДА: Введи ШИФР ДНЯ — одно слово, которое отражает твоё состояние сегодня.",
        "ПДА: Какое слово ты бы оставил на стене в бункере?",
        "ПДА: Одно слово. Как пароль в тетрадке выжившего.",
        "ПДА: Что отражает твоё состояние сейчас в одном слове?",
        "ПДА: Введи кодовое слово дня, сталкер.",
        "ПДА: Каким словом обозначишь сегодняшний день?",
        "ПДА: Введи ШИФР ДНЯ — одно слово, передающее суть текущего состояния.",
        "ПДА: Передай сигнал Зоне. Одним словом.",
        "ПДА: Одно слово. Как шрам, оставшийся после вылазки.",
        "ПДА: Введи ключ к себе. Зашифрованно, в одно слово."
        "ПДА: Введи шифр дня — кодовое слово для расшифровки состояния.",
        "ПДА: Активируй шифрослот. Одно ключевое слово.",
        "ПДА: Инициализация шифросессии. Ключ-пароль: одно слово.",
        "ПДА: Зона требует идентификатор. Введи ключевое слово дня."
    ]

    user_id = callback.from_user.id
    old_msg_id = user_state.get(user_id, {}).get("last_message_id")
    if old_msg_id:
        try:
            await callback.bot.delete_message(callback.message.chat.id, old_msg_id)
        except:
            pass

    msg = await callback.message.answer(random.choice(prompts))
    user_state.setdefault(user_id, {})["last_message_id"] = msg.message_id
