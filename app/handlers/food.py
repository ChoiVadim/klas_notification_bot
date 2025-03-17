import logging
from aiogram import Dispatcher, types
from aiogram.filters import Command

from app.strings import Strings
from app.keyboards import create_food_menu_keyboard
from app.services.food import get_today_school_food_menu
from app.utils.language_utils import get_user_language_with_fallback


async def show_school_food_menu(message: types.Message):
    try:
        user_lang = await get_user_language_with_fallback(message)

        await message.answer(
            await get_today_school_food_menu(user_lang),
            reply_markup=create_food_menu_keyboard(user_lang),
        )
        logging.info(f"User {message.from_user.id} used /menu command")
    except Exception as e:
        logging.error(f"Error in show_school_food_menu: {e}")
        await message.answer(Strings.get("unexpected_error", user_lang))


def register_handlers(dp: Dispatcher):
    dp.message.register(show_school_food_menu, Command("menu"))
