import logging
from aiogram.filters import Command
from aiogram import Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.utils.encryption import encrypt_password
from app.services.kw import KwangwoonUniversityApi
from app.database.database import delete_user, save_user
from app.strings import Strings, Language


# Define states for registration
class RegistrationStates(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()


async def cmd_register(message: types.Message, state: FSMContext):
    try:
        await state.set_state(RegistrationStates.waiting_for_username)
        await message.reply(Strings.get("enter_username", Language.EN))
    except Exception as e:
        logging.error(f"Error in cmd_register: {e}")
        await message.answer(Strings.get("unexpected_error", Language.EN))


async def process_username(message: types.Message, state: FSMContext):
    try:
        await state.update_data(username=message.text)
        await state.set_state(RegistrationStates.waiting_for_password)
        await message.answer(Strings.get("enter_password", Language.EN))
        await message.delete()
    except Exception as e:
        logging.error(f"Error in process_username: {e}")
        await message.answer(Strings.get("unexpected_error", Language.EN))


async def process_password(message: types.Message, state: FSMContext):
    try:
        user_data = await state.get_data()
        username = user_data["username"]
        password = message.text

        try:
            # Test credentials
            async with KwangwoonUniversityApi() as kw:
                isLogin = await kw.login(username, password)
                if not isLogin:
                    await message.answer(
                        Strings.get("invalid_credentials", Language.EN)
                    )
                    return

            # Save user credentials to the database
            user_id = str(message.from_user.id)
            encrypted_password = encrypt_password(password)
            if await save_user(user_id, username, encrypted_password):
                await message.answer(
                    Strings.get("registration_successful", Language.EN)
                )
            else:
                await message.answer(
                    Strings.get("failed_to_save_credentials", Language.EN)
                )

        except Exception as e:
            await message.answer(Strings.get("registration_failed", Language.EN))
        finally:
            await message.delete()
            await state.clear()
    except Exception as e:
        logging.error(f"Error in process_password: {e}")
        await message.answer(Strings.get("unexpected_error", Language.EN))


async def cmd_unregister(message: types.Message):
    try:
        await delete_user(str(message.from_user.id))
        await message.answer(Strings.get("unregistered", Language.EN))
    except Exception as e:
        logging.error(f"Error in cmd_unregister: {e}")
        await message.answer(Strings.get("unexpected_error", Language.EN))


def register_handlers(dp: Dispatcher):
    # Command handlers
    dp.message.register(cmd_register, Command("register"))
    dp.message.register(cmd_unregister, Command("unregister"))

    # State handlers
    dp.message.register(process_username, RegistrationStates.waiting_for_username)
    dp.message.register(process_password, RegistrationStates.waiting_for_password)
