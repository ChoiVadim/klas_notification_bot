import logging

from aiogram import Dispatcher, types
from app.services.food import (
    get_today_school_food_menu,
    get_tomorrow_school_food_menu,
    get_school_food_info,
)
from aiogram.exceptions import TelegramBadRequest

from app.strings import Strings, Language
from app.services.news import get_news
from app.keyboards import (
    create_food_menu_keyboard,
    create_back_to_food_menu_keyboard,
    create_news_keyboard,
)
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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
        elif callback_query.data == "filter_news":
            await callback_query.message.edit_text(
                "Choose a type of news", reply_markup=create_news_keyboard()
            )
        elif callback_query.data == "filter_foreigners_news":
            try:
                await callback_query.message.delete()
                news = await get_news("foreigners")
                for item in news[:3]:
                    date = item["date"]
                    title = item["title"]
                    link = item["link"]
                    await callback_query.message.answer(
                        f"📰 {title}\n{date}",
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [InlineKeyboardButton(text="Read more", url=link)]
                            ]
                        ),
                    )

            except Exception as e:
                logging.error(f"Failed to fetch news: {e}")
                await callback_query.message.reply(
                    "Failed to fetch news. Please try again later."
                )

        elif callback_query.data == "filter_all_news":
            try:
                await callback_query.message.delete()
                news = await get_news("all")
                for item in news[:5]:
                    date = item["date"]
                    title = item["title"]
                    link = item["link"]
                    await callback_query.message.answer(
                        f"📰 {title}\n{date}",
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [InlineKeyboardButton(text="Read more", url=link)]
                            ]
                        ),
                    )
            except Exception as e:
                logging.error(f"Failed to fetch news: {e}")
                await callback_query.message.reply(
                    "Failed to fetch news. Please try again later."
                )
    except TelegramBadRequest as e:
        logging.error(f"Bad request: {e}")
        await callback_query.message.reply(Strings.get("callback_error", Language.EN))
    except Exception as e:
        logging.error(f"Error in process_callback_query: {e}")
        await callback_query.message.reply(Strings.get("unexpected_error", Language.EN))


def register_handlers(dp: Dispatcher):
    dp.callback_query.register(process_callback_query)
