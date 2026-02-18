import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'token.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)



import googlesheets as gs
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from employment import r1


sheet = gs.Sheets("Example")
TOKEN = os.getenv("BOT_TOKEN")
dp = Dispatcher()


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_router(r1)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
