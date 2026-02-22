from aiogram import html
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram import F
from aiogram import Router
import services as ser

or_ch = Router()

class Form(StatesGroup):
    index = State()
    new_st = State()


@or_ch.callback_query(F.data == "order_change_status")
async def command_hub(callback: CallbackQuery):
    await callback.answer()
    try:
        res = ser.df_order
        if(res.empty):
            await callback.message.answer("Žádné rozkazy. ")
        else:
            
            msg = f"""
<b>Typ služby:</b> {res.iloc[0]["st"]}
<b>Datum:</b> {res.iloc[0]["data"]}
<b>Začátek:</b> {res.iloc[0]["startTime"]}
<b>Trvání:</b> {res.iloc[0]["dr"]}
<b>Cena:</b> {res.iloc[0]["price"]}
<b>Datum vytvoření:</b> {res.iloc[0]["created"]}
<b>Stav:</b> {res.iloc[0]["status"]}
<b>ID objednávky:</b> {res.iloc[0]["or_id"]}
<b>ID klienta:</b> {res.iloc[0]["cl_id"]}
"""
            await callback.message.answer(msg,
                reply_markup=get_slider_kb(0),
                parse_mode="HTML"
            )
    except Exception as e:
        print(e)
        await callback.message.answer("Došlo k chybě, počkejte prosím několik minut a zkuste to znovu...")


def get_slider_kb(index: int):
    builder = InlineKeyboardBuilder()
    order = ser.df_order
    if index > 0:
        builder.button(text="⬅️", callback_data=f"o_{index-1}")

    builder.button(text="Změnit stav", callback_data=f"order_change:{index}")
    if index < len(order) - 1:
        builder.button(text="➡️", callback_data=f"o_{index+1}")
    
    builder.adjust(2)
    return builder.as_markup()


@or_ch.callback_query(F.data.startswith("o_"))
async def slider(callback: CallbackQuery):
    await callback.answer()
    try:
        index = int(callback.data.split("_")[1])
        res = ser.df_order
        # защита от выхода за границы
        if index < 0:
            index = 0
        if index >= len(res):
            index = len(res)-1

        if(res.empty):
            await callback.message.answer("Žádné rozkazy.")
        else:
            msg = f"""
<b>Typ služby:</b> {res.iloc[index]["st"]}
<b>Datum:</b> {res.iloc[index]["data"]}
<b>Začátek:</b> {res.iloc[index]["startTime"]}
<b>Trvání:</b> {res.iloc[index]["dr"]}
<b>Cena:</b> {res.iloc[index]["price"]}
<b>Datum vytvoření:</b> {res.iloc[index]["created"]}
<b>Stav:</b> {res.iloc[index]["status"]}
<b>ID objednávky:</b> {res.iloc[index]["or_id"]}
<b>ID klienta:</b> {res.iloc[index]["cl_id"]}
"""
            await callback.message.edit_text( msg,
                    reply_markup=get_slider_kb(index),
                    parse_mode="HTML"
                )
    except Exception as e:
        print(e)
        await callback.message.answer("Došlo k chybě, počkejte prosím několik minut a zkuste to znovu...")



@or_ch.callback_query(F.data.startswith("order_change:"))
async def command_hub_change(callback: CallbackQuery,state : FSMContext):
    await callback.answer()
    await state.update_data(index=int(callback.data.split(":")[1]))
    await callback.message.answer("Napište nový status (scheduled/done/cancele):  ")
    await state.set_state(Form.new_st)

@or_ch.message(Form.new_st)
async def command_word_ask_date(message : Message, state : FSMContext):
    await state.update_data(new_st=message.text)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Zpět do centra",callback_data="hub_ad")]])
    await message.answer("Nyní máme vše uložené do tabulky.",reply_markup=keyboard)
    data = await state.get_data()
    ser.sheet.update_status(data["index"]+1,data["new_st"])
    await state.clear()