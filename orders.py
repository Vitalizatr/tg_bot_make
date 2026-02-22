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

ad_order = Router()

class Form(StatesGroup):
    st = State()
    date = State()
    startTime = State()
    duration = State()
    price = State()
    address = State()

@ad_order.callback_query(F.data == "order_add")
async def command_ask_st(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Napište typ služby")
    await state.set_state(Form.st)

@ad_order.message(Form.st)
async def command_word_ask_date(message : Message, state : FSMContext):
    await state.update_data(st=message.text)
    await message.answer("Napište datum ve formátu (dd.mm.yyyy)")
    await state.set_state(Form.date)

@ad_order.message(Form.date)
async def command_word_ask_startTime(message : Message, state : FSMContext):
    await state.update_data(date=message.text)
    await message.answer("Napište čas začátku služby: hh:mm")
    await state.set_state(Form.startTime)

@ad_order.message(Form.startTime)
async def command_word_duration(message : Message, state : FSMContext):
    await state.update_data(startTime=message.text)
    await message.answer("Napište délku služby")
    await state.set_state(Form.duration)

@ad_order.message(Form.duration)
async def command_word_price(message : Message, state : FSMContext):
    await state.update_data(duration=message.text)
    await message.answer("Napište cenu objednávky")
    await state.set_state(Form.price) 

@ad_order.message(Form.price)
async def command_word_address(message : Message, state : FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Napište adresu")
    await state.set_state(Form.address)  

@ad_order.message(Form.address)
async def command_result(message : Message, state : FSMContext):
    await state.update_data(address=message.text)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Zpět do hubu",callback_data="hub_ad")]])
    await message.answer("Vše bylo nyní uloženo do tabulky",reply_markup=keyboard)
    data = await state.get_data()
    ser.sheet.append_data(data["st"],data["date"],data["startTime"],data["duration"],data["price"],data["address"])
    await state.clear()