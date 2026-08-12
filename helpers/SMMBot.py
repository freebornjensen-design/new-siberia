import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Импортируем нашу исправленную функцию генерации
from ai_generator import generate_smm_content

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN env variable is not set")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class SMMState(StatesGroup):
    choosing_platform = State()
    typing_topic = State()


def get_platform_keyboard():
    buttons = [
        [InlineKeyboardButton(text="📱 Пост для Telegram", callback_data="platform_tg")],
        [InlineKeyboardButton(text="👥 Пост для ВКонтакте", callback_data="platform_vk")],
        [InlineKeyboardButton(text="🌐 Статья для Сайта (SEO)", callback_data="platform_seo_site")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Приветствую! Я твой персональный ИИ-копирайтер.\n"
        "Выбери площадку, для которой нужно сгенерировать контент:",
        reply_markup=get_platform_keyboard()
    )
    await state.set_state(SMMState.choosing_platform)


@dp.callback_query(F.data.startswith("platform_"), SMMState.choosing_platform)
async def process_platform_choice(callback: CallbackQuery, state: FSMContext):
    platform = callback.data.replace("platform_", "")
    await state.update_data(chosen_platform=platform)

    platform_names = {"tg": "Telegram", "vk": "ВКонтакте", "seo_site": "Сайта"}
    await callback.message.edit_text(
        f"Отлично! Пишем контент для *{platform_names[platform]}*.\n\n"
        "Отправь мне тезисы, ключевые слова или краткое описание темы:",
        parse_mode="Markdown"
    )
    await state.set_state(SMMState.typing_topic)
    await callback.answer()


# Интегрированный хэндлер с нарезкой длинных сообщений и валидацией HTML
@dp.message(SMMState.typing_topic, F.text)
async def process_topic_and_generate(message: Message, state: FSMContext):
    user_topic = message.text

    user_data = await state.get_data()
    platform = user_data.get("chosen_platform")

    waiting_message = await message.answer("⏳ *ИИ генерирует текст, секунду...*", parse_mode="Markdown")

    loop = asyncio.get_event_loop()
    generated_text = await loop.run_in_executor(None, generate_smm_content, platform, user_topic)

    await waiting_message.delete()

    # Защита от ломающих HTML-разметку символов
    clean_text = generated_text.replace("<", "&lt;").replace(">", "&gt;")

    # Лимит Telegram на одно сообщение — 4096 символов
    MAX_LENGTH = 4000

    if len(clean_text) <= MAX_LENGTH:
        await message.answer(
            f"🤖 <b>Готовый результат:</b>\n\n{clean_text}",
            parse_mode="HTML"
        )
    else:
        # Если текст огромный (например, статья), режем его на куски по абзацам
        chunks = []
        current_chunk = ""

        for paragraph in clean_text.split("\n"):
            if len(current_chunk) + len(paragraph) + 1 > MAX_LENGTH:
                chunks.append(current_chunk)
                current_chunk = paragraph
            else:
                current_chunk += "\n" + paragraph if current_chunk else paragraph
        if current_chunk:
            chunks.append(current_chunk)

        # Отправляем куски по очереди последовательно
        for i, chunk in enumerate(chunks):
            await message.answer(
                f"🤖 <b>Часть {i + 1}/{len(chunks)}:</b>\n\n{chunk}",
                parse_mode="HTML"
            )

    # Сброс состояния и вывод стартового меню
    await message.answer("Хочешь написать что-то еще? Выбери платформу:", reply_markup=get_platform_keyboard())
    await state.set_state(SMMState.choosing_platform)


async def main():
    print("Бот успешно запущен и готов к работе...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
