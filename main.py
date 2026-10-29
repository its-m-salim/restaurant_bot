from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext 
from keyboards import *
from states import router as state_router
from states import *
from service import *
from connection import *


import os
import asyncio


load_dotenv()

token_bot = os.getenv("BOT_TOKEN")

bot = Bot(token=token_bot)
dp = Dispatcher()



@dp.message(Command("start"))
async def start_bot(message: Message):
    usr = message.from_user
    user = await profile(message.from_user.id)
    if not user:
        await create_user(usr.username, usr.full_name, usr.id)
        password = usr.username or "admin13q"
        await set_password(password, usr.id)
        await message.answer(
            "👋 Добро пожаловать в рестарант!\n\n📚 Ищи книги, выбирай любимые категории и открывай новые истории.\n\n👇 Выбери действие в меню.",
            reply_markup=main_kb,
        )
        return
    if user["is_admin"]:
        await message.answer(
            "🛠 С возвращением, администратор!\n\n📚 Все возможности читателя и инструменты управления — в меню ниже.",
            reply_markup=admin_kb,
        )
        return
    await message.answer(
        f"✨ С возвращением, {usr.full_name}!\n\n📖 Что будем читать сегодня? Выбирай действие в меню ниже.",
        reply_markup=main_kb,
    )


@dp.message(F.text == "Menu")
@dp.message(Command("menu"))
async def show_menu(message: Message):

    categories = await get_category_btn()

    await message.answer("select category ", reply_markup=categories)


async def main():
    print("Бот запущен")
    dp.include_router(state_router)
    await create_tables()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    