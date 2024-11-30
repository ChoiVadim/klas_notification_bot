from aiogram import Dispatcher, types
from aiogram.filters import Command
from app.services.food import get_today_school_food_menu
from app.keyboards import create_food_menu_keyboard


async def show_school_food_menu(message: types.Message):
    await message.answer(
        await get_today_school_food_menu(), reply_markup=create_food_menu_keyboard()
    )


def register_handlers(dp: Dispatcher):
    dp.message.register(show_school_food_menu, Command("menu"))
