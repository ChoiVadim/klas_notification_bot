import logging
from aiogram import Dispatcher, types
from aiogram.filters import Command

from app.strings import Strings
from app.keyboards import create_news_keyboard
from app.utils.language_utils import get_user_language_with_fallback


async def cmd_news(message: types.Message):
    try:
        user_lang = await get_user_language_with_fallback(message)

        logging.info(f"User {message.from_user.id} used /news command")
        await message.answer(
            Strings.get("choose_news_type", user_lang),
            reply_markup=create_news_keyboard(user_lang),
        )
        await message.delete()
    except Exception as e:
        logging.error(f"Error in cmd_news: {e}")
        await message.answer(Strings.get("unexpected_error", user_lang))


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_news, Command("news"))
