from aiogram import html
from aiogram.filters import CommandStart,Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F 
from aiogram.types import Message
from aiogram import Router
from main import sheet, User


r2 = Router()


user = None

@r2.message(Command("admin"))
async def command_admin(message: Message) -> None:
    res = sheet.Ad_search(str(message.from_user.id))
    global user
    keyboard2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Зайти в аккаунт",callback_data="hub_ad")]])
    if(res): 
        await message.answer(f"""Привет, {html.bold(message.from_user.full_name)}! вы есть в базе. Можете сразу зайти """,reply_markup = keyboard1)
        user = User(str(message.from_user.id),res[0].ID,True)
    else:
        await message.answer(f"""Привет, {html.bold(message.from_user.full_name)}! вы лох {message.from_user.id} """,reply_markup = keyboard2)