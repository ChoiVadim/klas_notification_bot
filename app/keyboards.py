from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from app.strings import Strings, Language


def create_quick_access_keyboard(user_lang: Language):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📋 Todos"),
                KeyboardButton(text="🔍 QR"),
            ]
        ],
        resize_keyboard=True,
        is_persistent=True,
        one_time_keyboard=False,
        input_field_placeholder=Strings.get("input_field_placeholder", user_lang)
    )
    return keyboard


def create_todos_keyboard():
    todos_keyboard = InlineKeyboardBuilder()
    todos_keyboard.button(text="Show only 3 days left", callback_data="filter_3")
    todos_keyboard.button(text="Show only 1 week left", callback_data="filter_7")
    todos_keyboard.adjust(2)
    return todos_keyboard.as_markup()


def create_language_keyboard():
    language_keyboard = InlineKeyboardBuilder()
    language_keyboard.button(text=Language.EN.value, callback_data="language_en")
    language_keyboard.button(text=Language.KO.value, callback_data="language_ko")
    language_keyboard.button(text=Language.RU.value, callback_data="language_ru")
    language_keyboard.adjust(1)
    return language_keyboard.as_markup()


def create_food_menu_keyboard(user_lang: Language):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=Strings.get("tomorrow_menu", user_lang), callback_data="filter_tomorrow"
    )
    builder.button(
        text=Strings.get("info", user_lang), callback_data="filter_food_info"
    )
    builder.adjust(1)  # Adjust the number of buttons per row

    # Convert the builder to InlineKeyboardMarkup
    return builder.as_markup()


def create_back_to_food_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙", callback_data="filter_today")
    builder.adjust(1)

    return builder.as_markup()


def create_news_keyboard(user_lang: Language):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=Strings.get("foreigners_news", user_lang),
        callback_data="filter_foreigners_news",
    )
    builder.button(
        text=Strings.get("all_news", user_lang), callback_data="filter_all_news"
    )
    builder.adjust(2)

    return builder.as_markup()


def create_donation_keyboard(user_lang: Language):
    builder = InlineKeyboardBuilder()
    
    # Add different donation amount options
    builder.button(text="1⭐", callback_data="donate_1")
    builder.button(text="5⭐", callback_data="donate_5")
    builder.button(text="10⭐", callback_data="donate_10")
    builder.button(text="20⭐", callback_data="donate_20")
    builder.button(text="50⭐", callback_data="donate_50")
    builder.button(text="100⭐", callback_data="donate_100")
    
    # Adjust to have 3 buttons per row
    builder.adjust(3)
    
    return builder.as_markup()
