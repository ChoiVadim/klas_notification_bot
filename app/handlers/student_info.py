import aiohttp
import logging
from pathlib import Path

from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

from app.database.database import get_user, get_user_language
from app.utils.encryption import decrypt_password
from app.services.kw import KwangwoonUniversityApi
from app.strings import Strings, Language


async def cmd_info(message: types.Message):
    try:
        user_lang = await get_user_language(str(message.from_user.id))
        if not user_lang:
            user_lang = Language.EN
        logging.info(f"User {message.from_user.id} used /info command")
        # Check if user is registered
        user = await get_user(str(message.from_user.id))
        if not user:
            await message.answer(Strings.get("need_to_register", user_lang))
            return

        async with KwangwoonUniversityApi() as kw:
            await kw.login(user.username, decrypt_password(user.encrypted_password))
            student_info = await kw.get_student_info()

            if not student_info:
                await message.answer(
                    Strings.get("failed_to_fetch_student_info", user_lang)
                )
                return

            photos_dir = Path("images/photos")
            photos_dir.mkdir(exist_ok=True)
            photo_path = photos_dir / f"student_{message.from_user.id}.jpg"

            if not photo_path.exists():
                student_photo_url = await kw.get_student_photo_url()
                async with aiohttp.ClientSession() as session:
                    async with session.get(student_photo_url) as response:
                        if response.status == 200:
                            with open(photo_path, "wb") as f:
                                f.write(await response.read())
                        else:
                            photo_path = "images/logo.jpg"

            student_photo_file = FSInputFile(str(photo_path))

            msg = Strings.get(
                "student_info",
                user_lang,
                uid=student_info["uid"],
                name=student_info["name"],
                major=student_info["major"],
                grade=student_info["grade"],
                semester=student_info["semester"],
                total_credits=student_info["credits"]["total"],
                required_credits=student_info["credits"]["required"],
                major_credits_total=student_info["major_credits"]["total"],
                major_credits_required=student_info["major_credits"]["required"],
                elective_credits_total=student_info["elective_credits"]["total"],
                elective_credits_required=student_info["elective_credits"]["required"],
                average_score=student_info["average_score"],
                credits_per_semester=student_info["credits_for_each_semester"],
                major_credits_per_semester=student_info[
                    "major_credits_for_each_semester"
                ],
            )

            await message.reply_photo(photo=student_photo_file, caption=msg)

    except Exception as e:
        logging.error(f"Unexpected error in cmd_info: {e}")
        await message.answer(Strings.get("unexpected_error", user_lang))


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_info, Command("info"))
