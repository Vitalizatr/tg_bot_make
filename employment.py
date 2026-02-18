from aiogram import html
from aiogram.filters import CommandStart,Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F 
from aiogram.types import Message
from aiogram import Router
from main import sheet, User

r1 = Router()

user = None
orders = []

@r1.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    res = sheet.Em_search(str(message.from_user.id))
    global user
    keyboard1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Зарегестрироватся",callback_data="reg")]])
    keyboard2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Зайти в аккаунт",callback_data="hub_em")]])
    if(res): 
        await message.answer(f"""Привет, {html.bold(message.from_user.full_name)}! вы есть в базе. Можете сразу зайти """,reply_markup = keyboard2)
        user = User(str(message.from_user.id),res[0].ID,False)
    else:
        await message.answer(f"""Привет, {html.bold(message.from_user.full_name)}! вы лох {message.from_user.id} """,reply_markup = keyboard1)

@r1.callback_query(F.data == "hub_em")
async def command_hub(callback: CallbackQuery):
    await callback.answer()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Посмотреть свое расписание",callback_data="sch_em")],
                                                     [InlineKeyboardButton(text="Изменить свой статус",callback_data="status_em")]
                                                     ])
    await callback.message.answer("Ну что ",reply_markup=keyboard)


@r1.callback_query(F.data == "status_em")
async def command_status_em(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(f"Поменяли статус на: {sheet.update_data(user.ID+1)}")




@r1.callback_query(F.data == "sch_em")
async def command_sch_em(callback: CallbackQuery):
    await callback.answer()
    global order
    order = sheet.search_by_or_em(user.ID)
    order_info = sheet.search_by_sc(user.ID)
    if(order == []):
        await callback.message.answer("У вас нету заданий) ")
    else:
        await callback.message.answer(
            f""" 
            Заказ под номером : {orders[0].Or_Id};      Время Начала: {order_info[0].startTime}
            Роль : {orders[0].role};        Время Конца: {order_info[0].endTime}
            Тип Оплаты : {orders[0].rt};        Адрес: {order_info[0].address}
            Стоимость : {orders[0].rv};         Дата: {order_info[0].date}
    """,
            reply_markup=get_slider_kb(0)
        )




def get_slider_kb(index: int):
    builder = InlineKeyboardBuilder()

    if index > 0:
        builder.button(text="⬅️", callback_data=f"order_{index-1}")

    if index < len(orders) - 1:
        builder.button(text="➡️", callback_data=f"order_{index+1}")

    builder.adjust(2)
    return builder.as_markup()


@r1.callback_query(F.data.startswith("order_"))
async def slider(callback: CallbackQuery):
    index = int(callback.data.split("_")[1])

    # защита от выхода за границы
    if index < 0:
        index = 0
    if index >= len(orders):
        index = len(orders) - 1

    await callback.message.edit_text(
        f""" 
            Заказ под номером : {orders[index].Or_Id};      Время Начала: {orders[index].startTime}
            Роль : {orders[index].role};        Время Конца: {orders[index].endTime}
            Тип Оплаты : {orders[index].rt};        Адрес: {orders[index].address}
            Стоимость : {orders[index].rv};         Дата: {orders[index].date}
    """,
        reply_markup=get_slider_kb(index)
    )

    await callback.answer()




@r1.callback_query(F.data == "reg")
async def command_reg(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Регистрация")