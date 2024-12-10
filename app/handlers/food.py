import logging
from aiogram import Dispatcher, types
from aiogram.filters import Command

from app.strings import Strings, Language
from app.keyboards import create_food_menu_keyboard
from app.services.food import get_today_school_food_menu
from app.database.database import get_user_language


async def show_school_food_menu(message: types.Message):
    try:
        user_lang = await get_user_language(str(message.from_user.id))
        if not user_lang:
            user_lang = Language.EN

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
