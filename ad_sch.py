from aiogram import html
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message
from aiogram import F
from aiogram import Router
import services as ser

ad_sch = Router()


@ad_sch.callback_query(F.data == "sch_ad")
async def command_hub(callback: CallbackQuery):
    await callback.answer()
    try:
        res = ser.df_summary
        if(res.empty):
            await callback.message.answer("Nejsou žádní zaměstnanci.")
        else:
            
            msg = f"""
<b>Číslo zaměstnance:</b> {res.iloc[0]["em_id"]}
<b>Jméno:</b> {res.iloc[0]["name"]}
<b>Telefon:</b> {res.iloc[0]["phone"]}
<b>Status:</b> {res.iloc[0]["status"]}
<b>Počet objednávek:</b> {res.iloc[0]["order_count"]}
"""
            await callback.message.answer(msg,
                reply_markup=get_slider_kb(0),
                parse_mode="HTML"
            )
    except Exception as e:
        print(e)
        await callback.message.answer("Došlo k chybě. Počkejte několik minut a zkuste to znovu...")


def get_slider_kb(index: int):
    builder = InlineKeyboardBuilder()
    order = ser.df_summary
    if index > 0:
        builder.button(text="⬅️", callback_data=f"emp_{index-1}")

    if index < len(order) - 1:
        builder.button(text="➡️", callback_data=f"emp_{index+1}")

    builder.adjust(2)
    return builder.as_markup()


@ad_sch.callback_query(F.data.startswith("emp_"))
async def slider(callback: CallbackQuery):
    await callback.answer()
    try:
        index = int(callback.data.split("_")[1])
        res = ser.df_summary
        # защита от выхода за границы
        if index < 0:
            index = 0
        if index >= len(res):
            index = len(res)-1

        if(res.empty):
            await callback.message.answer("Vaše úkoly byly odstraněny.")
        else:
            msg = f"""
<b>Číslo zaměstnance:</b> {res.iloc[index]["em_id"]}
<b>Jméno:</b> {res.iloc[index]["name"]}
<b>Telefon:</b> {res.iloc[index]["phone"]}
<b>Status:</b> {res.iloc[index]["status"]}
<b>Počet objednávek:</b> {res.iloc[index]["order_count"]}
"""
            await callback.message.edit_text( msg,
                    reply_markup=get_slider_kb(index),
                    parse_mode="HTML"
                )
    except Exception as e:
        print(e)
        await callback.message.answer("Došlo k chybě. Počkejte několik minut a zkuste to znovu...")