import os
import logging
import asyncio

from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

from app.services.qr import get_qr
from app.strings import Strings, Language
from app.database.database import get_library_user, get_user_language
from app.utils.encryption import decrypt_password
from app.services.library import search_book


async def cmd_qr(message: types.Message):
    try:
        user_lang = await get_user_language(str(message.from_user.id))
        if not user_lang:
            user_lang = Language.EN
        user = await get_library_user(str(message.from_user.id))
        if not user:
            await message.answer(Strings.get("library_user_not_found", user_lang))
            return

        qr_code_path = await get_qr(
            user.username, user.phone_number, decrypt_password(user.encrypted_password)
        )

        try:
            qr_photo = await message.answer_photo(FSInputFile(qr_code_path))
            logging.info(f"User {message.from_user.id} used /qr command")
            await message.delete()
            await asyncio.sleep(30)
            await qr_photo.delete()
        except Exception as e:
            logging.error(f"Error in reply_photo: {e}")
            await message.answer(Strings.get("unexpected_error", user_lang))

    except Exception as e:
        logging.error(f"Error in cmd_qr: {e}")
        await message.answer(Strings.get("unexpected_error", user_lang))


async def cmd_find_book(message: types.Message):
    try:
        user_lang = await get_user_language(str(message.from_user.id)) 
        if not user_lang:
            user_lang = Language.EN
        logging.info(f"User {message.from_user.id} used /search command")
        query = message.text.split("/search")[1]
        if not query:
            await message.answer(
                Strings.get("please_enter_book_name", user_lang)
            )
            return

        list_of_books = await search_book(query)

        if not list_of_books:
            await message.answer(Strings.get("no_books_found", user_lang))
            return
        for book in list_of_books:
            message_text = f"📚 {book[0]}\n\n"
            for info in book[2]:
                message_text += (
                    f"📍 {info['location']}\n📦 {info['book_shell_number']}\n"
                )
                if info["status"]:
                    message_text += f"🔄 {info['status']} {info['return_date']}\n"
                else:
                    message_text += "🔄 Available\n"
                message_text += "\n"
            if book[1]:
                await message.answer_photo(book[1], caption=message_text)
            else:
                await message.answer(message_text)

    except Exception as e:
        logging.error(f"Error in cmd_find_book: {e}")
        await message.answer(Strings.get("unexpected_error", user_lang))


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_qr, Command("qr"))
    dp.message.register(cmd_find_book, Command("search"))
