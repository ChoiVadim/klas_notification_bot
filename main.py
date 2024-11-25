import os
import json
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from kw_api import KwangwoonUniversityApi

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
    await message.answer(
        "Welcome! Please register to use the service.\nUse /register to start registration."
    )


@dp.message(Command("register"))
async def cmd_register(message: types.Message, state: FSMContext):
    await state.set_state(RegistrationStates.waiting_for_username)
    await message.reply("Please enter your Kwangwoon University username:")


@dp.message(RegistrationStates.waiting_for_username)
async def process_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(RegistrationStates.waiting_for_password)
    await message.answer("Please enter your password:")
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
                    "Invalid credentials. Please check your username and password and try again with /register"
                )
                return

        # Save user credentials
        user_id = str(message.from_user.id)
        try:
            with open("users.json", "r") as f:
                users = json.load(f)
        except FileNotFoundError:
            users = {}

        users[user_id] = {"username": username, "password": password}

        with open("users.json", "w") as f:
            json.dump(users, f)

        await message.answer(
            "Registration successful! You will now receive notifications."
        )

    except Exception as e:
        await message.answer(
            "Registration failed. Please check your credentials and try again with /register"
        )
    finally:
        await message.delete()
        await state.clear()


async def send_notification(message: str, user_id: str, urgency_level: int):
    try:
        emoji = TIME_THRESHOLDS.get(urgency_level, "📌")
        prefix = f"{emoji} {urgency_level} hour{'s' if urgency_level > 1 else ''} remaining!\n\n"

        await bot.send_message(chat_id=user_id, text=prefix + message)
    except Exception as e:
        print(f"Error sending notification: {e}")


async def check_todos():
    while True:
        try:
            with open("users.json", "r") as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Create empty users.json file if it doesn't exist or is malformed
            users = {}
            with open("users.json", "w") as f:
                json.dump(users, f)
            continue  # Skip to next iteration since we have no users

        for user_id, credentials in users.items():
            async with KwangwoonUniversityApi() as kw:
                await kw.login(credentials["username"], credentials["password"])
                todo_list = await kw.get_todo_list()

                # Dictionary to store messages for each time threshold
                threshold_messages = {
                    threshold: "" for threshold in TIME_THRESHOLDS.keys()
                }

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
                            # Let's check the first assignment only for now
                            for assignment in assignments:
                                left_time = assignment["left_time"].seconds
                                days_left = assignment["left_time"].days
                                hours_left = left_time // 3600

                                if abs(days_left) > 0:
                                    continue

                                # Check against each threshold
                                for threshold in TIME_THRESHOLDS.keys():
                                    # If the time left is less than the threshold but greater than
                                    # the next lower threshold (if any)
                                    if hours_left <= threshold and hours_left > (
                                        max(
                                            [
                                                t
                                                for t in TIME_THRESHOLDS.keys()
                                                if t < threshold
                                            ],
                                            default=0,
                                        )
                                    ):
                                        threshold_messages[threshold] += (
                                            f"{emoji} {subject_name}: "
                                            f"{assignment_type.title()} you have "
                                            f"{hours_left} hour{'s' if hours_left != 1 else ''} "
                                            f"and {left_time % 3600 // 60} minutes left😭\n"
                                        )

                # Send notifications for each threshold that has messages
                for threshold, message in threshold_messages.items():
                    if message:
                        await send_notification(message, user_id, threshold)
                        # Add small delay between notifications to prevent flooding
                        await asyncio.sleep(1)

        # Wait for 15 minutes before checking again
        await asyncio.sleep(900)  # 900 seconds = 15 minutes


async def main():
    print("Starting todo check service...")
    # Start polling in parallel with todo checking
    await asyncio.gather(dp.start_polling(bot), check_todos())


if __name__ == "__main__":
    asyncio.run(main())
