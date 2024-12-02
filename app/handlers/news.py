import logging
from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.keyboards import create_news_keyboard


async def cmd_news(message: types.Message):
    await message.answer(
        "📰 Choose a type of news 📰", reply_markup=create_news_keyboard()
    )


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_news, Command("news"))
