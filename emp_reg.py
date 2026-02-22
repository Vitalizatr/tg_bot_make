from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,CallbackQuery
from aiogram import F
from aiogram import Router

emp_reg = Router()

@emp_reg.callback_query(F.data == "hub_em")
async def command_hub(callback: CallbackQuery):
    await callback.answer()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Zobrazit svůj rozvrh",callback_data="sch_em")],
                                                     [InlineKeyboardButton(text="Změnit svůj status",callback_data="status_em")]
                                                     ])
    await callback.message.answer("Váš hub. Zde si můžete zobrazit svůj rozvrh a změnit status ve svém účtu.",reply_markup=keyboard)