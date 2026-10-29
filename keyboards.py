from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from service import *


main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📚 Все книги"), KeyboardButton(text="Menu")],
        [KeyboardButton(text="🔐 Войти как администратор"), KeyboardButton(text="❓ Помощь")],
    ],
    resize_keyboard=True,
)


admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📚 Все книги"), KeyboardButton(text="➕ Добавить книгу")],
        [KeyboardButton(text="delete dish"), KeyboardButton(text="✏️ Изменить dish")],
        [ KeyboardButton(text="❓ Помощь")]
    ],
    resize_keyboard=True,
)



async def get_category_btn():
    data = await get_categories()
    keyboards = []

    for ct in data:
        keyboards.append([InlineKeyboardButton(text=ct['name'], callback_data=f"category_{ct['id']}")])
    
    keyboards.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)

    return keyboard


async def get_ct_dishes_btn(cat_id):
    data = await get_category_dishes(cat_id)
    keyboards = []

    for dish in data:
        keyboards.append([InlineKeyboardButton(text=dish['name'], callback_data=f"dish_{dish['id']}")])
    keyboards.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keyboard


async def get_order_btn():

    keyboard = [
        [InlineKeyboardButton(text="order", callback_data="new_order"), InlineKeyboardButton(text="back", callback_data="back")],
        [InlineKeyboardButton(text="cancel", callback_data="cancel")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return keyboard

async def get_dishes_all_btn():
    data = await get_all_dishes()
    keyboards = []

    for index, dish in enumerate(data, start=1):
        keyboards.append([InlineKeyboardButton(text=f"{index}.{dish['name']}", callback_data=f"dishd_{dish['id']}")])
    keyboards.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keyboard
