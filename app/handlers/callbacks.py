import logging

from aiogram import Dispatcher, types
from app.services.food import (
    get_today_school_food_menu,
    get_tomorrow_school_food_menu,
    get_school_food_info,
)
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.database.database import set_user_language, get_user_language
from app.strings import Strings, Language
from app.services.news import get_news
from app.keyboards import (
    create_food_menu_keyboard,
    create_back_to_food_menu_keyboard,
    create_news_keyboard,
)


async def process_callback_query(callback_query: types.CallbackQuery):
    try:
        user_lang = await get_user_language(callback_query.from_user.id)
        if not user_lang:
            user_lang = Language.EN

        if callback_query.data == "filter_food_info":
            await callback_query.message.edit_text(
                await get_school_food_info(user_lang),
                reply_markup=create_back_to_food_menu_keyboard(),
            )
        elif callback_query.data == "filter_today":
            await callback_query.message.edit_text(
                await get_today_school_food_menu(user_lang),
                reply_markup=create_food_menu_keyboard(user_lang),
            )
        elif callback_query.data == "filter_tomorrow":
            await callback_query.message.edit_text(
                await get_tomorrow_school_food_menu(user_lang),
                reply_markup=create_back_to_food_menu_keyboard(),
            )
        elif callback_query.data == "filter_news":
            await callback_query.message.edit_text(
                Strings.get("choose_news_type", user_lang),
                reply_markup=create_news_keyboard(user_lang),
            )

        # Language change
        elif callback_query.data == "language_en":
            await set_user_language(callback_query.from_user.id, "en")
            await callback_query.message.edit_text(
                Strings.get("language_changed", Language.EN),
            )
        elif callback_query.data == "language_ko":
            await set_user_language(callback_query.from_user.id, "ko")
            await callback_query.message.edit_text(
                Strings.get("language_changed", Language.KO),
            )
        elif callback_query.data == "language_ru":
            await set_user_language(callback_query.from_user.id, "ru")
            await callback_query.message.edit_text(
                Strings.get("language_changed", Language.RU),
            )

        # News
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
                                [
                                    InlineKeyboardButton(
                                        text=Strings.get("read_more", user_lang),
                                        url=link,
                                    )
                                ]
                            ]
                        ),
                    )

            except Exception as e:
                logging.error(f"Failed to fetch news: {e}")
                await callback_query.message.reply(
                    Strings.get("failed_to_fetch_news", user_lang)
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
                                [
                                    InlineKeyboardButton(
                                        text=Strings.get("read_more", user_lang),
                                        url=link,
                                    )
                                ]
                            ]
                        ),
                    )
            except Exception as e:
                logging.error(f"Failed to fetch news: {e}")
                await callback_query.message.reply(
                    Strings.get("failed_to_fetch_news", user_lang)
                )
    except TelegramBadRequest as e:
        logging.error(f"Bad request: {e}")
        await callback_query.message.reply(Strings.get("callback_error", user_lang))
    except Exception as e:
        logging.error(f"Error in process_callback_query: {e}")
        await callback_query.message.reply(Strings.get("unexpected_error", user_lang))


def register_handlers(dp: Dispatcher):
    dp.callback_query.register(process_callback_query)
