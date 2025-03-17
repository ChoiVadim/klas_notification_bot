import logging

from aiogram import Dispatcher, types
from app.services.food import (
    get_today_school_food_menu,
    get_tomorrow_school_food_menu,
    get_school_food_info,
)
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.database.database import set_user_language
from app.strings import Strings, Language
from app.services.news import get_news
from app.keyboards import (
    create_food_menu_keyboard,
    create_back_to_food_menu_keyboard,
    create_news_keyboard,
)
from app.utils.language_utils import get_user_language_with_fallback


async def process_callback_query(callback_query: types.CallbackQuery):
    try:
        user_lang = await get_user_language_with_fallback(callback_query)

        # Handle donation amount selection
        if callback_query.data.startswith("donate_"):
            try:
                # Extract the amount from the callback data
                amount = int(callback_query.data.split("_")[1])
                
                # Send invoice with the selected amount
                await callback_query.message.edit_text(
                    f"Processing donation of {amount}⭐..."
                )
                
                await callback_query.bot.send_invoice(
                    chat_id=callback_query.from_user.id,
                    title=Strings.get("donate_title", user_lang),
                    description=Strings.get("donate_description", user_lang),
                    prices=[types.LabeledPrice(label=f"Donation (${amount})", amount=amount)],
                    currency="XTR",
                    payload=f"donate_{amount}",
                    provider_token="",  # Your payment provider token
                )
                
                logging.info(f"User {callback_query.from_user.id} selected donation amount: ${amount}")
                await callback_query.answer()
                return
                
            except Exception as e:
                logging.error(f"Error processing donation: {e}")
                await callback_query.message.edit_text(Strings.get("unexpected_error", user_lang))
                return

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
            await set_user_language(callback_query.from_user.id, "EN")
            await callback_query.message.edit_text(
                Strings.get("language_changed", Language.EN),
            )
        elif callback_query.data == "language_ko":
            await set_user_language(callback_query.from_user.id, "KO")
            await callback_query.message.edit_text(
                Strings.get("language_changed", Language.KO),
            )
        elif callback_query.data == "language_ru":
            await set_user_language(callback_query.from_user.id, "RU")
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
