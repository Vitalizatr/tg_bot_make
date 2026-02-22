from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from aiogram import Router
import services as ser


emp_sch = Router()

@emp_sch.callback_query(F.data == "status_em")
async def command_status_em(callback: CallbackQuery):
    await callback.answer()
    try:
        res = ser.df_employees[ser.df_employees["tgId"] == str(callback.from_user.id)]
        if not res.empty:
            ID = res.iloc[0]["em_id"]
            await callback.message.answer(f"Status byl změněn na: {ser.sheet.update_data(str(int(ID)+1))}")
        else:
            await callback.message.answer("Nejste v databázi.")
    except Exception as e:
        print(e)
        await callback.message.answer("Došlo k chybě. Počkejte několik minut a zkuste to znovu...")




@emp_sch.callback_query(F.data == "sch_em")
async def command_sch_em(callback: CallbackQuery):
    await callback.answer()
    try:
        res = ser.df_employees[ser.df_employees["tgId"] == str(callback.from_user.id)]
        ID = res.iloc[0]["em_id"]
        order = ser.df_orders[ser.df_orders["em_id"] == str(ID)]
        order_info = ser.df_schedule[ser.df_schedule["em_id"] == str(ID)]
        if(order.empty):
            await callback.message.answer("Nemáte žádné úkoly.")
        else:
            
            msg = f"""
<b>Objednávka číslo:</b> {order.iloc[0]["or_id"]}
<b>Čas začátku:</b> {order_info.iloc[0]["st"]}
<b>Role:</b> {order.iloc[0]["role"]}
<b>Čas konce:</b> {order_info.iloc[0]["et"]}
<b>Typ platby:</b> {order.iloc[0]["rt"]}
<b>Adresa:</b> {order_info.iloc[0]["address"]}
<b>Cena:</b> {order.iloc[0]["rv"]}
<b>Datum:</b> {order_info.iloc[0]["date"]}
"""
            await callback.message.answer(msg,
                reply_markup=get_slider_kb(0,ID),
                parse_mode="HTML"
            )
    except Exception as e:
        print(e)
        await callback.message.answer("Došlo k chybě. Počkejte několik minut a zkuste to znovu...")




def get_slider_kb(index: int,ID):
    builder = InlineKeyboardBuilder()
    order = ser.df_orders[ser.df_orders["em_id"] == str(ID)]
    if index > 0:
        builder.button(text="⬅️", callback_data=f"e_{index-1}")

    if index < len(order) - 1:
        builder.button(text="➡️", callback_data=f"e_{index+1}")

    builder.adjust(2)
    return builder.as_markup()


@emp_sch.callback_query(F.data.startswith("e_"))
async def slider(callback: CallbackQuery):
    await callback.answer()
    try:
        index = int(callback.data.split("_")[1])
        res = ser.df_employees[ser.df_employees["tgId"] == str(callback.from_user.id)]
        ID = res.iloc[0]["em_id"]
        order = ser.df_orders[ser.df_orders["em_id"] == str(ID)]
        order_info = ser.df_schedule[ser.df_schedule["em_id"] == str(ID)]
        # защита от выхода за границы
        if index < 0:
            index = 0
        if index >= len(order) and index >= len(order_info):
            index = min(len(order) - 1,len(order_info)-1)

        if(order.empty):
            await callback.message.answer("Vaše úkoly byly odstraněny.")
        else:
            msg = f"""
<b>Objednávka číslo:</b> {order.iloc[index]["or_id"]}
<b>Čas začátku:</b> {order_info.iloc[index]["st"]}
<b>Role:</b> {order.iloc[index]["role"]}
<b>Čas konce:</b> {order_info.iloc[index]["et"]}
<b>Typ platby:</b> {order.iloc[index]["rt"]}
<b>Adresa:</b> {order_info.iloc[index]["address"]}
<b>Cena:</b> {order.iloc[index]["rv"]}
<b>Datum:</b> {order_info.iloc[index]["date"]}
"""
            await callback.message.edit_text( msg,
                    reply_markup=get_slider_kb(index,ID),
                    parse_mode="HTML"
                )
    except Exception as e:
        print(e)
        await callback.message.answer("Došlo k chybě. Počkejte několik minut a zkuste to znovu...")