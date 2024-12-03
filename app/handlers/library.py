import os
import logging
import asyncio

from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

from app.services.qr import get_qr
from app.strings import Strings, Language
from app.database.database import get_library_user
from app.utils.encryption import decrypt_password
from app.services.library import search_book


async def cmd_qr(message: types.Message):
    try:
        user = await get_library_user(str(message.from_user.id))
        if not user:
            await message.answer(Strings.get("library_user_not_found", Language.EN))
            return

        qr_code_path = await get_qr(
            user.username, user.phone_number, decrypt_password(user.encrypted_password)
        )

        try:
            qr_photo = await message.answer_photo(FSInputFile(qr_code_path))
            await message.delete()
            await asyncio.sleep(30)
            await qr_photo.delete()
        except Exception as e:
            logging.error(f"Error in reply_photo: {e}")
            await message.answer(Strings.get("unexpected_error", Language.EN))

    except Exception as e:
        logging.error(f"Error in cmd_qr: {e}")
        await message.answer(Strings.get("unexpected_error", Language.EN))
    finally:
        if os.path.exists(qr_code_path):
            os.remove(qr_code_path)


async def cmd_find_book(message: types.Message):
    try:
        query = message.text.split("/search")[1]
        if not query:
            await message.answer("Please enter a book name after /search command.")
            return

        list_of_books = await search_book(query)
        for book in list_of_books:
            # (title, image_url, location, status, return_date)
            message_text = f"📚 {book[0]}\n📍 Location: {book[2]}\n🔄 Status: {book[3]} till {book[4]}"
            await message.answer_photo(book[1], caption=message_text)
    except Exception as e:
        logging.error(f"Error in cmd_find_book: {e}")
        await message.answer(Strings.get("unexpected_error", Language.EN))


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_qr, Command("qr"))
    dp.message.register(cmd_find_book, Command("search"))
