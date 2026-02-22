import os
import asyncio
import logging
import sys
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,CallbackQuery
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram import html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import services as ser


from emp_reg import emp_reg
from emp_sch import emp_sch
from ad_sch import ad_sch
from ad_reg import ad_reg
from orders import ad_order
from or_ch import or_ch

TOKEN = os.getenv("BOT_TOKEN")
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    try:
        res = ser.df_employees[ser.df_employees["tgId"] == str(message.from_user.id)]
        keyboard2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Přihlásit se do účtu",callback_data="hub_em")]])
        if(not res.empty): 
            await message.answer(f"""Ahoj, {html.bold(message.from_user.full_name)}! Jste v databázi. Můžete se hned přihlásit.""",reply_markup = keyboard2)
        else:
            await message.answer(f"""Ahoj, {html.bold(message.from_user.full_name)}! Nejste evidován jako zaměstnanec. Požádejte o přidání do databáze. 
                                Vaše Telegram ID: {message.from_user.id} """)
    except Exception as e:
        print(e)
        await message.answer("Došlo k chybě. Počkejte několik minut a zkuste to znovu...")

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    asyncio.create_task(ser.refresh_data_5_min())
    asyncio.create_task(ser.refresh_data_1_min())
    asyncio.create_task(ser.refresh_data_10_min())    

    
    dp.include_router(emp_reg)
    dp.include_router(emp_sch)
    dp.include_router(ad_reg)
    dp.include_router(ad_sch)
    dp.include_router(ad_order)
    dp.include_router(or_ch)




    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
