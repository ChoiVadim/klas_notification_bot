import logging
from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.services.news import get_news


async def cmd_news(message: types.Message):
    try:
        news = await get_news()
        for item in news[:3]:
            date = item["date"]
            title = item["title"]
            link = item["link"]
            await message.answer(
                f"📰 {title}\n{date}",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="Read more", url=link)]]
                ),
            )
    except Exception as e:
        logging.error(f"Failed to fetch news: {e}")
        await message.reply("Failed to fetch news. Please try again later.")


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_news, Command("news"))
