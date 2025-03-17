import logging
from aiogram.filters import Command
from aiogram import Dispatcher, types

from app.strings import Strings
from app.database.database import get_user
from app.utils.encryption import decrypt_password
from app.services.kw import KwangwoonUniversityApi
from app.utils.language_utils import get_user_language_with_fallback

async def show_all_assignments(message: types.Message):
    try:
        user_lang = await get_user_language_with_fallback(message)

        logging.info(f"User {message.from_user.id} used /show command")
        user_id = str(message.from_user.id)
        user = await get_user(user_id)

        if not user:
            await message.answer(Strings.get("need_to_register", user_lang))
            return

        async with KwangwoonUniversityApi() as kw:
            await kw.login(user.username, decrypt_password(user.encrypted_password))
            todo_list = await kw.get_todo_list()

            if not todo_list:
                await message.answer(Strings.get("no_assignments", user_lang))
                return

            # Assignment type emojis
            type_emojis = {
                "lectures": "📚",
                "homeworks": "📝",
                "quizzes": "🧠",
                "team_projects": "👥",
            }

            response = Strings.get("todo_list_header", user_lang)

            for subject in todo_list:
                subject_name = subject.get("name", "Unknown Subject")
                has_assignments = False

                subject_tasks = f"📘 {subject_name}\n"

                for assignment_type, emoji in type_emojis.items():
                    assignments = subject["todo"].get(assignment_type, [])
                    if assignments:
                        has_assignments = True
                        subject_tasks += f"{emoji} {Strings.get(assignment_type, user_lang, count=len(assignments))}\n"

                        for assignment in assignments:
                            left_time = assignment["left_time"]
                            days = left_time.days
                            hours = left_time.seconds // 3600
                            minutes = (left_time.seconds % 3600) // 60

                            if days < 0 or hours < 0 or minutes < 0:
                                continue

                            time_str = ""
                            if days > 0:
                                time_str += f"{days}d "
                            if hours > 0:
                                time_str += f"{hours}h "
                            time_str += f"{minutes}m"

                            subject_tasks += (
                                f"  • {assignment.get('title', 'Untitled')}\n"
                                f"    {Strings.get('time_left', user_lang, time_str=time_str)}\n"
                            )
                subject_tasks += "\n\n"

                if has_assignments:
                    response += subject_tasks + "\n"

            if response == Strings.get("todo_list_header", user_lang):
                await message.answer(Strings.get("no_assignments", user_lang))
            else:
                # Split message if it's too long
                if len(response) > 4096:
                    for i in range(0, len(response), 4096):
                        await message.answer(response[i : i + 4096])
                else:
                    await message.answer(response)

    except Exception as e:
        logging.error(f"Error in show_all_assignments: {e}")
        await message.answer(Strings.get("unexpected_error", user_lang))


def register_handlers(dp: Dispatcher):
    dp.message.register(show_all_assignments, Command("show"))
