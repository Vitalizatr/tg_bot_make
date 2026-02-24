from aiogram import html
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,CallbackQuery
from aiogram.types import Message
from aiogram import F
from aiogram import Router
import services as ser


ad_reg = Router()


@ad_reg.message(Command("admin"))
async def command_admin(message: Message) -> None:
    try:
        res = ser.df_admins[ser.df_admins == str(message.from_user.id)]
        keyboard2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Přihlásit se do účtu",callback_data="hub_ad")]])
        if(not res.empty): 
            await message.answer(f"""Ahoj, {html.bold(message.from_user.full_name)}! Jste v databázi administrátorů. Můžete vstoupit do hubu.""",reply_markup=keyboard2)
        else:
            await message.answer(f"""Ahoj, {html.bold(message.from_user.full_name)}! Nejste evidován jako administrátor. Požádejte o přidání do databáze. 
                                Vaše Telegram ID: {message.from_user.id} """)
    except Exception as e:
        print(e)
        await message.answer(f"""Došlo k chybě. Počkejte několik minut a zkuste to znovu... """)
        

@ad_reg.callback_query(F.data == "hub_ad")
async def command_hub(callback: CallbackQuery):
    await callback.answer()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Zobrazit rozvrh zaměstnanců",callback_data="sch_ad")],
                                                     [InlineKeyboardButton(text="Přidat objednávku",callback_data="order_add")],
                                                     [InlineKeyboardButton(text="Změnit stav objednávky",callback_data="order_change_status")]
                                                     ])
    await callback.message.answer("Váš hub. Zde můžete přidat nebo odstranit objednávku. Také můžete zobrazit rozvrh zaměstnanců.",reply_markup=keyboard)
