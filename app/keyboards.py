from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_todos_keyboard():
    todos_keyboard = InlineKeyboardBuilder()
    todos_keyboard.button(text="Show only 3 days left", callback_data="filter_3")
    todos_keyboard.button(text="Show only 1 week left", callback_data="filter_7")
    todos_keyboard.adjust(2)
    return todos_keyboard.as_markup()


def create_food_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Tomorrow's Menu", callback_data="filter_tomorrow")
    builder.button(text="Info", callback_data="filter_food_info")
    builder.adjust(1)  # Adjust the number of buttons per row

    # Convert the builder to InlineKeyboardMarkup
    return builder.as_markup()


def create_back_to_food_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙", callback_data="filter_today")
    builder.adjust(1)

    return builder.as_markup()


def create_news_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="For Foreigners", callback_data="filter_foreigners_news")
    builder.button(text="All", callback_data="filter_all_news")
    builder.adjust(2)

    return builder.as_markup()
