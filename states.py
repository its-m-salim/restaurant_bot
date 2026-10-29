from aiogram import  Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext 
from service import *
from connection import connection_db
from keyboards import *
from aiogram.utils.media_group import MediaGroupBuilder


router = Router()



class get_order(StatesGroup):
    get_order_count = State()
    get_order_table = State()
    get_order_name = State()


class delete_dish(StatesGroup):
    get_dish_id = State()




@router.message(F.text == "🗑 Удалить книгу")
@router.message(Command("del"))
async def delete(message: Message, state: FSMContext):
    user = await profile(message.from_user.id)
    # if not user["is_admin"]:
    #     await message.answer("⛔ Эта команда доступна только администратору.")
    #     return

    buttons = await get_dishes_all_btn()
    await message.answer("Выберите книгу, которую хотите удалить", reply_markup=buttons)
    await state.set_state(delete_dish.get_dish_id)


@router.callback_query(delete_dish().get_dish_id, F.data.startswith("dishd_"))
async def get_book_id(callback: CallbackQuery, state: FSMContext):

    # if is_cancel(message.text):
    #     await message.answer("↩️ Действие отменено.")
    #     await state.clear()
    #     return
    
    dish_id = callback.data.split("_")[1]

    if await delete_dishs(dish_id):
        await callback.message.answer("✅ Книга успешно удалена!")
        await state.clear()
    else:
        await callback.message.answer("⚠️ Что-то пошло не так. Попробуйте позже.")
        await state.clear()





@router.callback_query(F.data.startswith("category_"))
async def show_dishes(callback: CallbackQuery):

    category_id = callback.data.split("_")[1]

    dishes = await get_ct_dishes_btn(category_id)
    if not dishes.inline_keyboard:
        await callback.answer("No dishes in this category yet")
        return
    
    await callback.message.answer("choose dish", reply_markup=dishes)


@router.callback_query(F.data.startswith("dish_"))
async def show_dish(callback: CallbackQuery, state: FSMContext):

    dish_id = callback.data.split("_")[1]

    await state.update_data(dish_id = dish_id)
    order_btn = await get_order_btn()
    dish_photo = await get_dish_pic(dish_id)

    # if not dish_photo:
    #     await callback.message.answer("No pics for this dish yet")
    # else:
    #     await callback.message.answer_photo(photo=dish_photo["photo_file_id"])

    dish = await  about_dish(dish_id)
    await callback.message.answer(f"""
name: {dish["name"]}
price: {dish["price"]}
caption: {dish["caption"]}
""", reply_markup=order_btn)

   
   
@router.callback_query(F.data == "new_order")
async def take_order(callback: CallbackQuery, state: FSMContext):

    await state.set_state(get_order.get_order_count)
    await callback.message.answer("Введите количество заказа")

   
   

@router.message(get_order.get_order_count)
async def get_order_count(message: Message, state: FSMContext):

    if not message.text.isdigit():
        await message.answer("must be a number! try again")
        return
    
    quantity = message.text

    await state.update_data(quantity = quantity)

    await message.answer("введите номер стола")
    await state.set_state(get_order.get_order_table)
   
   
@router.message(get_order.get_order_table)
async def get_order_count(message: Message, state: FSMContext):

    if not message.text.isdigit():
        await message.answer("must be a number! try again")
        return
    
    table = message.text

    await state.update_data(table = table)

    await message.answer("введите нимя заказчика")
    await state.set_state(get_order.get_order_name)


@router.message(get_order.get_order_name)
async def get_order_count(message: Message, state: FSMContext):
    
    name = message.text

    await state.update_data(name = name)

    data = await state.get_data()

    if await take_new_order(message.from_user.id, data['dish_id'], data['quantity'], data['table'], data['name']):
        await message.answer("order created successfuly")
        return

    await message.answer("not order no")
    await state.clear()

   
   
   
    # await state.set_state(get_order.get_dish_id)
    # await state.update_data(dish = dish_id)
    # await state.set_state(get_order.get_order_count)


