import logging
from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.keyboards import create_news_keyboard


async def cmd_news(message: types.Message):
    logging.info(f"User {message.from_user.id} used /news command")
    await message.answer(
        "📰 Choose a type of news 📰", reply_markup=create_news_keyboard()
    )
    await message.delete()


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_news, Command("news"))
