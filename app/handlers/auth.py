from aiogram.filters import Command
from aiogram import Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.utils.encryption import encrypt_password
from app.services.kw import KwangwoonUniversityApi
from app.database.database import delete_user, save_user


# Define states for registration
class RegistrationStates(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()


async def cmd_register(message: types.Message, state: FSMContext):
    await state.set_state(RegistrationStates.waiting_for_username)
    await message.reply("🔄 Please enter your Kwangwoon University username:")


async def process_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(RegistrationStates.waiting_for_password)
    await message.answer("🔑 Please enter your password:")
    await message.delete()


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


async def cmd_unregister(message: types.Message):
    await delete_user(str(message.from_user.id))
    await message.answer("You have been unregistered from the bot.")


def register_handlers(dp: Dispatcher):
    # Command handlers
    dp.message.register(cmd_register, Command("register"))
    dp.message.register(cmd_unregister, Command("unregister"))

    # State handlers
    dp.message.register(process_username, RegistrationStates.waiting_for_username)
    dp.message.register(process_password, RegistrationStates.waiting_for_password)
