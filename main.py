import os
import json
import asyncio
import aiohttp
from pathlib import Path

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import FSInputFile

from encryptor import encrypt_password, decrypt_password
from kw_api import KwangwoonUniversityApi
from llm import generate_response
from scrapers import (
    get_today_school_food_menu,
    get_tomorrow_school_food_menu,
    get_school_food_info,
)
from database import init_db, save_user, get_user, get_all_users, delete_user
from keyboards import create_food_menu_keyboard, create_back_to_food_menu_keyboard

load_dotenv()


# Define states for registration
class RegistrationStates(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()


storage = MemoryStorage()
dp = Dispatcher(storage=storage)
bot = Bot(token=os.getenv("BOT_TOKEN"))

# Define time thresholds in hours and their corresponding emoji indicators
TIME_THRESHOLDS = {
    1: "🚨",  # Critical
    2: "⚠️",  # Warning
    3: "⏰",  # Alert
    6: "📢",  # Notice
    12: "ℹ️",  # Info
    24: "📅",  # Day notice
}


# Add registration handlers
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    caption = f"""Welcome, {message.from_user.first_name}!👋
This bot is made for the students of Kwangwoon University 🏫
This bot will track your all assignments and notify you when they are less than 24 hours left 🧭

/register to start registration
/unregister to delete all your information from the bot
/show If you want to see all your tasks to do 🔍
/info If you want to see your graduation information 📝

❗ You need to register to use main features. This bot will encrypt your password and username. I do not save your credentials in visible form. So don't worry about your privacy.
I would appreciate if you could help me to improve this bot.
Send me any feedback or suggestions to @tsoivadim 💬
And i will try to improve this bot as soon as possible!

Made with ❤️ by @tsoivadim
"""
    photo = FSInputFile("images/logo.jpg")
    await message.reply_photo(
        photo=photo,
        caption=caption,
    )


@dp.message(Command("info"))
async def cmd_info(message: types.Message):
    async with KwangwoonUniversityApi() as kw:
        try:
            with open("users.json", "r") as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            await message.answer("You need to register first. Use /register to start.")
            return

        user_id = str(message.from_user.id)
        credentials = users.get(user_id)

        if not credentials:
            await message.answer("You need to register first. Use /register to start.")
            return

        await kw.login(credentials["username"], credentials["password"])
        student_info = await kw.get_student_info()

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


@dp.message(Command("register"))
async def cmd_register(message: types.Message, state: FSMContext):
    await state.set_state(RegistrationStates.waiting_for_username)
    await message.reply("🔄 Please enter your Kwangwoon University username:")


@dp.message(RegistrationStates.waiting_for_username)
async def process_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(RegistrationStates.waiting_for_password)
    await message.answer("🔑 Please enter your password:")
    await message.delete()


@dp.message(RegistrationStates.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    username = user_data["username"]
    password = message.text

    try:
        # Test credentials
        async with KwangwoonUniversityApi() as kw:
            isLogin = await kw.login(username, password)
            if not isLogin:
                await message.answer(
                    "🚫 Invalid credentials. Please check your username and password and try again with /register"
                )
                return

        # Save user credentials to the database
        user_id = str(message.from_user.id)
        encrypted_password = encrypt_password(password)
        if await save_user(user_id, username, encrypted_password):
            await message.answer(
                "Registration successful! You will now receive notifications."
            )
        else:
            await message.answer(
                "Failed to save your credentials. Please try again later."
            )

    except Exception as e:
        await message.answer(
            "Registration failed. Please check your credentials and try again with /register"
        )
    finally:
        await message.delete()
        await state.clear()


@dp.message(Command("unregister"))
async def cmd_unregister(message: types.Message):
    await delete_user(str(message.from_user.id))
    await message.answer("You have been unregistered from the bot.")


@dp.message(Command("donate"))
async def cmd_donate(message: types.Message):
    await message.reply_invoice(
        title="Buy me a coffee!😁",
        description="Thank you for using my bot!",
        prices=[types.LabeledPrice(label="Donation", amount=1)],
        currency="XTR",
        payload="donate",
        provider_token="",
    )


@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message(Command("refund"))
async def cmd_refund(message: types.Message):
    try:
        # Check if the message is a reply to a payment message
        if (
            not message.reply_to_message
            or not message.reply_to_message.successful_payment
        ):
            await message.answer(
                "Please reply to a payment message to request a refund."
            )
            return

        payment = message.reply_to_message.successful_payment

        # Attempt to refund the payment
        result = await bot.refund_star_payment(
            user_id=message.from_user.id,
            telegram_payment_charge_id=payment.telegram_payment_charge_id,
        )

        if result:
            await message.answer("✅ Refund has been processed successfully.")
        else:
            await message.answer(
                "❌ Refund request was not successful. Please try again later."
            )

    except Exception as e:
        await message.answer(f"❌ Error processing refund: {str(e)}")


@dp.message(Command("menu"))
async def show_school_food_menu(message: types.Message):
    await message.answer(
        await get_today_school_food_menu(), reply_markup=create_food_menu_keyboard()
    )


@dp.message(Command("show"))
async def show_all_assignments(message: types.Message):
    user_id = str(message.from_user.id)
    user = await get_user(user_id)

    if not user:
        await message.answer("You need to register first. Use /register to start.")
        return

    async with KwangwoonUniversityApi() as kw:
        await kw.login(user.username, decrypt_password(user.encrypted_password))
        todo_list = await kw.get_todo_list()

        if not todo_list:
            await message.answer("No assignments found or failed to fetch assignments.")
            return

        # Assignment type emojis
        type_emojis = {
            "lectures": "📚",
            "homeworks": "📝",
            "quizzes": "🧠",
            "team_projects": "👥",
        }

        response = "📋 Your Todo List:\n\n"

        for subject in todo_list:
            subject_name = subject.get("name", "Unknown Subject")
            has_assignments = False

            subject_tasks = f"📘 {subject_name}"

            for assignment_type, emoji in type_emojis.items():
                assignments = subject["todo"].get(assignment_type, [])
                if assignments:
                    has_assignments = True
                    subject_tasks += f"\n{emoji} {assignment_type.title()}:\n"

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
                            f"    ⏰ Time remaining: {time_str}\n"
                        )
            subject_tasks += "\n\n"

            if has_assignments:
                response += subject_tasks + "\n"

        if response == "📋 Your Todo List:\n\n":
            await message.answer("No pending assignments! 🎉")
        else:
            # Split message if it's too long
            if len(response) > 4096:
                for i in range(0, len(response), 4096):
                    await message.answer(response[i : i + 4096])
            else:
                await message.answer(response)


@dp.callback_query()
async def process_callback_query(callback_query: types.CallbackQuery):
    if callback_query.data == "filter_3":
        await callback_query.message.edit_text(
            "Showing only assignments with less than 3 days left..."
        )
    elif callback_query.data == "filter_7":
        await callback_query.message.edit_text(
            "Showing only assignments with less than 1 week left..."
        )
    elif callback_query.data == "filter_food_info":
        await callback_query.message.edit_text(
            await get_school_food_info(),
            reply_markup=create_back_to_food_menu_keyboard(),
        )
    elif callback_query.data == "filter_today":
        await callback_query.message.edit_text(
            await get_today_school_food_menu(),
            reply_markup=create_food_menu_keyboard(),
        )
    elif callback_query.data == "filter_tomorrow":
        await callback_query.message.edit_text(
            await get_tomorrow_school_food_menu(),
            reply_markup=create_back_to_food_menu_keyboard(),
        )


async def send_notification(message: str, user_id: str, urgency_level: int):
    try:
        emoji = TIME_THRESHOLDS.get(urgency_level, "📌")
        prefix = f"{emoji} {urgency_level} hour{'s' if urgency_level > 1 else ''} remaining!\n\n"

        await bot.send_message(chat_id=user_id, text=prefix + message)
    except Exception as e:
        print(f"Error sending notification: {e}")


async def check_todos():
    notification_tracker = {}

    while True:
        users = await get_all_users()

        for user in users:
            user_id = user.user_id
            if user_id not in notification_tracker:
                notification_tracker[user_id] = {}

            async with KwangwoonUniversityApi() as kw:
                await kw.login(user.username, decrypt_password(user.encrypted_password))
                todo_list = await kw.get_todo_list()

                threshold_messages = {
                    threshold: "" for threshold in TIME_THRESHOLDS.keys()
                }

                if not todo_list:
                    logging.info(f"No todo list found for user {user_id}")
                    continue

                for subject in todo_list:
                    subject_name = subject.get("name", "Unknown Subject")

                    # Assignment type emojis
                    type_emojis = {
                        "lectures": "📚",
                        "homeworks": "📝",
                        "quizzes": "🧠",
                        "team_projects": "🚧",
                    }

                    # Check each type of assignment
                    for assignment_type, emoji in type_emojis.items():
                        assignments = subject["todo"].get(assignment_type, [])
                        if assignments:
                            for assignment in assignments:
                                # Create unique assignment identifier
                                assignment_id = f"{subject_name}_{assignment_type}_{assignment.get('title', '')}"

                                # Initialize assignment tracker if not exists
                                if assignment_id not in notification_tracker[user_id]:
                                    notification_tracker[user_id][assignment_id] = set()

                                left_time = assignment["left_time"].seconds
                                days_left = assignment["left_time"].days
                                hours_left = left_time // 3600

                                if abs(days_left) > 0:
                                    continue

                                for threshold in TIME_THRESHOLDS.keys():
                                    if (
                                        hours_left <= threshold
                                        and hours_left
                                        > max(
                                            [
                                                t
                                                for t in TIME_THRESHOLDS.keys()
                                                if t < threshold
                                            ],
                                            default=0,
                                        )
                                        and threshold
                                        not in notification_tracker[user_id][
                                            assignment_id
                                        ]
                                    ):  # Check if notification wasn't sent

                                        threshold_messages[threshold] += (
                                            f"{emoji} {subject_name}: "
                                            f"{assignment_type.title()} you have "
                                            f"{hours_left} hour{'s' if hours_left != 1 else ''} "
                                            f"and {left_time % 3600 // 60} minutes left😭\n"
                                        )
                                        # Mark this threshold as notified for this assignment
                                        notification_tracker[user_id][
                                            assignment_id
                                        ].add(threshold)

                # Send notifications for each threshold that has messages
                for threshold, message in threshold_messages.items():
                    if message:
                        await send_notification(message, user_id, threshold)
                        await asyncio.sleep(1)

            # Clean up old assignments from tracker
            current_assignments = {
                f"{subject['name']}_{type_}_{assignment.get('title', '')}"
                for subject in todo_list
                for type_ in type_emojis.keys()
                for assignment in subject["todo"].get(type_, [])
            }

            notification_tracker[user_id] = {
                assignment_id: thresholds
                for assignment_id, thresholds in notification_tracker[user_id].items()
                if assignment_id in current_assignments
            }

        await asyncio.sleep(900)


@dp.message()
async def other_message(message: types.Message):
    if message.content_type == types.ContentType.SUCCESSFUL_PAYMENT:
        await message.answer("Thank you for your donation!")
    else:
        await bot.send_message(
            message.from_user.id, await generate_response(message.text)
        )


async def main():
    logging.info("Starting todo check service...")
    await init_db()  # Initialize the database
    # Start polling in parallel with todo checking
    await asyncio.gather(dp.start_polling(bot), check_todos())


if __name__ == "__main__":
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename="log.txt",
        filemode="a",
        encoding="UTF-8",
    )
    asyncio.run(main())
