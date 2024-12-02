import os
import logging
from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

from app.services.qr import get_qr
from app.strings import Strings, Language
from app.database.database import get_library_user
from app.utils.encryption import decrypt_password


async def cmd_qr(message: types.Message):
    try:
        user = await get_library_user(str(message.from_user.id))
        if not user:
            await message.answer(Strings.get("user_not_found", Language.EN))
            return

        qr_code_path = await get_qr(
            user.username, user.phone_number, decrypt_password(user.encrypted_password)
        )
        try:
            await message.reply_photo(FSInputFile(qr_code_path))
        except Exception as e:
            logging.error(f"Error in reply_photo: {e}")
            await message.answer(Strings.get("unexpected_error", Language.EN))

    except Exception as e:
        logging.error(f"Error in cmd_qr: {e}")
        await message.answer(Strings.get("unexpected_error", Language.EN))
    finally:
        if os.path.exists(qr_code_path):
            os.remove(qr_code_path)


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_qr, Command("qr"))
