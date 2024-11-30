import aiohttp
from pathlib import Path

from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

from app.database.database import get_user
from app.utils.encryption import decrypt_password
from app.services.kw import KwangwoonUniversityApi


async def cmd_info(message: types.Message):
    async with KwangwoonUniversityApi() as kw:
        user_id = str(message.from_user.id)
        user = await get_user(user_id)

        if not user:
            await message.answer("You need to register first. Use /register to start.")
            return

        await kw.login(user.username, decrypt_password(user.encrypted_password))
        student_info = await kw.get_student_info()

        if not student_info:
            await message.answer(
                "Failed to fetch student information. Please try again later."
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

        msg = (
            f"📝 UID: {student_info['uid']} \n"
            f"👨‍🎓 Name: {student_info['name']} \n"
            f"Major: {student_info['major']}\n"
            f"Grade: {student_info['grade']} Semester: {student_info['semester']}\n"
            f"🎯 Total Credits: {student_info['credits']['total']}/{student_info['credits']['required']}\n"
            f"Major Credits: {student_info['major_credits']['total']}/{student_info['major_credits']['required']}\n"
            f"Elective Credits: {student_info['elective_credits']['total']}/{student_info['elective_credits']['required']}\n"
            f"Average Score: {student_info['average_score']} 📈\n\n"
            f"❗ Recommendation: take at least {student_info['credits_for_each_semester']} credits each semester and {student_info['major_credits_for_each_semester']} major credits each semester to graduate on time!\n\n"
            f"P.S. As a foreigner student, we don't need to care about elective credits but if you have TOPIC less than 4, you need to take Korean language classes and get TOPIC 4 at least before graduation 🇰🇷"
        )

        await message.reply_photo(photo=student_photo_file, caption=msg)


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_info, Command("info"))
