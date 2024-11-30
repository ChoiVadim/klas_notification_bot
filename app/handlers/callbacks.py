import logging

from aiogram import Dispatcher, types
from app.services.food import (
    get_today_school_food_menu,
    get_tomorrow_school_food_menu,
    get_school_food_info,
)
from app.strings import Strings, Language
from app.keyboards import create_food_menu_keyboard, create_back_to_food_menu_keyboard


async def process_callback_query(callback_query: types.CallbackQuery):
    try:
        if callback_query.data == "filter_food_info":
            await callback_query.message.edit_text(
                await get_school_food_info(),
                reply_markup=create_back_to_food_menu_keyboard(),
            )
        elif callback_query.data == "filter_today":
            await callback_query.message.edit_text(
                await get_today_school_food_menu(),
                reply_markup=create_food_menu_keyboard(),
            )
        elif callback_query.data == "filter_tomorrow":
            await callback_query.message.edit_text(
                await get_tomorrow_school_food_menu(),
                reply_markup=create_back_to_food_menu_keyboard(),
            )
    except Exception as e:
        logging.error(f"Error in process_callback_query: {e}")
        await callback_query.message.answer(
            Strings.get("unexpected_error", Language.EN)
        )


def register_handlers(dp: Dispatcher):
    dp.callback_query.register(process_callback_query)
