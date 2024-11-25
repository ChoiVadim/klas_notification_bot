import os
import json
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import FSInputFile

from kw_api import KwangwoonUniversityApi
from llm import generate_advice

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
This bot is made for the students of Kwangwoon University.
Will track your assignments and notify you when they are less than 24 hours left.

You want to see all your tasks to do?
🔍 Use /show to see your all tasks to do.

You need to register to use main features.
🔄 Use /register to start registration.

If you have any questions, you can ask me anything!
💬 Use me as a normal chat.


Made with ❤️ by @tsoivadim
☕️ Buy me a coffee /donate 
"""
    photo = FSInputFile("images/logo.jpg")
    await message.reply_photo(
        photo=photo,
        caption=caption,
    )


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


# @dp.message(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
# async def process_successful_payment(message: types.Message):
#     if message.content_type == types.ContentType.SUCCESSFUL_PAYMENT:
#         await message.answer("Thank you for your donation!")


@dp.message(Command("refund"))
async def cmd_refund(message: types.Message):
    await message.answer(
        "To request a refund, please contact @tsoivadim directly with your transaction ID."
    )


@dp.message(Command("show"))
async def show_all_assignments(message: types.Message):
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


async def send_notification(message: str, user_id: str, urgency_level: int):
    try:
        emoji = TIME_THRESHOLDS.get(urgency_level, "📌")
        prefix = f"{emoji} {urgency_level} hour{'s' if urgency_level > 1 else ''} remaining!\n\n"

        await bot.send_message(chat_id=user_id, text=prefix + message)
    except Exception as e:
        print(f"Error sending notification: {e}")


async def check_todos():
    # Add notification tracking dictionary at the start of the function
    notification_tracker = (
        {}
    )  # Format: {user_id: {assignment_id: set(sent_thresholds)}}

    while True:
        try:
            with open("users.json", "r") as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users = {}
            with open("users.json", "w") as f:
                json.dump(users, f)
            continue

        for user_id, credentials in users.items():
            # Initialize user's tracker if not exists
            if user_id not in notification_tracker:
                notification_tracker[user_id] = {}

            async with KwangwoonUniversityApi() as kw:
                await kw.login(credentials["username"], credentials["password"])
                todo_list = await kw.get_todo_list()

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
    await bot.send_message(message.from_user.id, await generate_advice(message.text))


async def main():
    logging.info("Starting todo check service...")
    # Start polling in parallel with todo checking
    await asyncio.gather(dp.start_polling(bot), check_todos())


if __name__ == "__main__":
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename="log.txt",
        filemode="w",
        encoding="UTF-8",
    )
    asyncio.run(main())
