from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import os

async def notify_users(user_ids: list, text: str):
    bot = Bot(
        token=os.getenv("BOT_TOKEN"),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    for user_id in user_ids:
        try:
            await bot.send_message(chat_id=user_id, text=text)
        except Exception as e:
            print(f"Ошибка при отправке {user_id}: {e}")

    await bot.session.close()