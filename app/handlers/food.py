import logging
from aiogram import Dispatcher, types
from aiogram.filters import Command

from app.strings import Strings, Language
from app.keyboards import create_food_menu_keyboard
from app.services.food import get_today_school_food_menu


async def show_school_food_menu(message: types.Message):
    try:
        await message.answer(
            await get_today_school_food_menu(),
            reply_markup=create_food_menu_keyboard(),
        )
    except Exception as e:
        logging.error(f"Error in show_school_food_menu: {e}")
        await message.answer(Strings.get("unexpected_error", Language.EN))


def register_handlers(dp: Dispatcher):
    dp.message.register(show_school_food_menu, Command("menu"))
