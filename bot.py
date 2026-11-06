import asyncio
import logging
import os

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.enums import ChatAction
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

SYSTEM_PROMPT = """
Ты заботливый AI-психолог.

Твоя задача:
- поддерживать человека
- отвечать тепло и по-доброму
- задавать уточняющие вопросы
- помогать успокоиться
- быть естественным и человечным

Отвечай кратко, но тепло.
Используй эмодзи иногда.
"""

DISCLAIMER = (
    "⚠️ Важно:\n"
    "Я являюсь AI-ботом и не заменяю профессионального психолога.\n\n"
    "Если тебе становится хуже или нужна срочная помощь:\n"
    "📞 Россия: 112 (экстренные службы)\n"
    "📞 Телефон доверия: 8-800-2000-122\n\n"
    "Ты не один(одна) — помощь доступна 💙"
)

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🚀 Start")
        ],
        [
            KeyboardButton(text="😰 Тревога"),
            KeyboardButton(text="😔 Грусть")
        ],
        [
            KeyboardButton(text="😡 Злость"),
            KeyboardButton(text="💤 Выгорание")
        ],
        [
            KeyboardButton(text="🧘 Успокоиться")
        ]
    ],
    resize_keyboard=True
)

user_memory = {}
@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Привет 👋\n\n"
        "Я AI-помощник психологической поддержки 💙\n\n"
        "Выбери эмоцию ниже или напиши сообщение.\n\n"
        f"{DISCLAIMER}",
        reply_markup=main_keyboard
    )

@dp.message(lambda message: message.text == "🚀 Start")
async def start_button_handler(message: Message):
    await message.answer(
        "Готов начать диалог 💙\n"
        "Напиши, что тебя беспокоит или выбери эмоцию ниже.",
        reply_markup=main_keyboard
    )

@dp.message(lambda message: message.voice)
async def voice_handler(message: Message):
    try:
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        file = await bot.get_file(message.voice.file_id)
        downloaded_file = await bot.download_file(file.file_path)

        with open("voice.ogg", "wb") as f:
            f.write(downloaded_file.read())

        audio_file = open("voice.ogg", "rb")

        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

        user_text = transcript.text

        await message.answer(f"🎤 Вы сказали:\n\n{user_text}")

        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ]
        )

        ai_reply = response.choices[0].message.content
        await message.answer(ai_reply)

    except Exception as e:
        await message.answer(f"Ошибка голосового 😢\n{e}")


@dp.message(lambda message: message.text)
async def chat_handler(message: Message):
    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

    user_id = message.from_user.id
    user_text = message.text

    if not user_text:
        return

    if user_id not in user_memory:
        user_memory[user_id] = []

    user_memory[user_id].append({
        "role": "user",
        "content": user_text
    })

    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *user_memory[user_id]
            ]
        )

        ai_reply = response.choices[0].message.content

        user_memory[user_id].append({
            "role": "assistant",
            "content": ai_reply
        })

        await message.answer(ai_reply)

        text_lower = user_text.lower()

        video_data = {
            "трев": {
                "title": "Как справиться с тревогой",
                "url": "https://rutube.ru/video/a9f927c39cfd09e9fbc906650c5ff32a/"
            },
            "груст": {
                "title": "Как выйти из грусти",
                "url": "https://m.vkvideo.ru/video-129000999_456242811?from=search"
            },
            "выгор": {
                "title": "Видео про выгорание",
                "url": "https://yandex.ru/video/touch/preview/8372711610267492499"
            },
            "стресс": {
                "title": "Как снизить стресс",
                "url": "https://yandex.ru/video/touch/preview/3230947493703592846"
            }
        }

        for keyword, data in video_data.items():
            if keyword in text_lower:

                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="📺 Смотреть видео",
                                url=data["url"]
                            )
                        ]
                    ]
                )

                await message.answer(
                    f"🎥 {data['title']}",
                    reply_markup=keyboard
                )
                break

    except Exception as e:
        await message.answer(f"Ошибка: {e}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())