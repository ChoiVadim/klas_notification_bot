import logging
from aiogram.filters import Command
from aiogram import Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.utils.encryption import encrypt_password
from app.services.kw import KwangwoonUniversityApi
from app.services.qr import library_login, get_secret_key
from app.database.database import (
    delete_user,
    save_user,
    save_library_user,
    get_user_language,
)
from app.strings import Strings, Language


# Define states for registration
class RegistrationStates(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()


class LibraryRegistrationStates(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()
    waiting_for_phone_number = State()


async def cmd_register(message: types.Message, state: FSMContext):
    try:
        user_lang = await get_user_language(str(message.from_user.id))
        if not user_lang:
            user_lang = Language.EN

        await state.set_state(RegistrationStates.waiting_for_username)
        await message.answer(Strings.get("enter_username", user_lang))
        await message.delete()
    except Exception as e:
        logging.error(f"Error in cmd_register: {e}")
        await message.answer(Strings.get("unexpected_error", user_lang))
        await state.clear()


async def process_username(message: types.Message, state: FSMContext):
    try:
        user_lang = await get_user_language(str(message.from_user.id))
        if not user_lang:
            user_lang = Language.EN

        await state.update_data(username=message.text)
        await state.set_state(RegistrationStates.waiting_for_password)
        await message.answer(Strings.get("enter_password", user_lang))
        await message.delete()
    except Exception as e:
        logging.error(f"Error in process_username: {e}")
        await message.answer(Strings.get("unexpected_error", user_lang))
        await state.clear()


async def process_password(message: types.Message, state: FSMContext):
    try:
        user_lang = await get_user_language(str(message.from_user.id))
        if not user_lang:
            user_lang = Language.EN

        user_data = await state.get_data()
        username = user_data["username"]
        password = message.text

        try:
            # Test credentials
            async with KwangwoonUniversityApi() as kw:
                isLogin = await kw.login(username, password)
                if not isLogin:
                    await message.answer(Strings.get("invalid_credentials", user_lang))
                    return

            # Save user credentials to the database
            user_id = str(message.from_user.id)
            encrypted_password = encrypt_password(password)
            if await save_user(user_id, username, encrypted_password):
                await message.answer(Strings.get("registration_successful", user_lang))
                logging.info(f"User {user_id} registered successfully")
            else:
                await message.answer(
                    Strings.get("failed_to_save_credentials", user_lang)
                )

        except Exception as e:
            await message.answer(Strings.get("registration_failed", user_lang))
        finally:
            await message.delete()
            await state.clear()
    except Exception as e:
        logging.error(f"Error in process_password: {e}")
        await message.answer(Strings.get("unexpected_error", user_lang))


async def cmd_unregister(message: types.Message):
    try:
        user_lang = await get_user_language(str(message.from_user.id))
        if not user_lang:
            user_lang = Language.EN

        await delete_user(str(message.from_user.id))
        await message.answer(Strings.get("unregistered", user_lang))
        logging.info(f"User {message.from_user.id} unregistered")
        await message.delete()
    except Exception as e:
        logging.error(f"Error in cmd_unregister: {e}")
        await message.answer(Strings.get("unexpected_error", user_lang))


async def cmd_library_register(message: types.Message, state: FSMContext):
    try:
        user_lang = await get_user_language(str(message.from_user.id))
        if not user_lang:
            user_lang = Language.EN

        await state.set_state(LibraryRegistrationStates.waiting_for_username)
        await message.answer(Strings.get("library_enter_username", user_lang))
        await message.delete()
    except Exception as e:
        logging.error(f"Error in cmd_library_register: {e}")
        await message.answer(Strings.get("unexpected_error", user_lang))


async def process_library_username(message: types.Message, state: FSMContext):
    try:
        user_lang = await get_user_language(str(message.from_user.id))
        if not user_lang:
            user_lang = Language.EN

        await state.update_data(username=message.text)
        await state.set_state(LibraryRegistrationStates.waiting_for_password)
        await message.answer(Strings.get("library_enter_password", user_lang))
        await message.delete()
    except Exception as e:
        logging.error(f"Error in process_library_username: {e}")
        await message.answer(Strings.get("unexpected_error", user_lang))


async def process_library_password(message: types.Message, state: FSMContext):
    try:
        user_lang = await get_user_language(str(message.from_user.id))
        if not user_lang:
            user_lang = Language.EN

        await state.update_data(password=message.text)
        await state.set_state(LibraryRegistrationStates.waiting_for_phone_number)
        await message.answer(Strings.get("enter_phone_number", user_lang))
        await message.delete()
    except Exception as e:
        logging.error(f"Error in process_library_password: {e}")
        await message.answer(Strings.get("unexpected_error", user_lang))


async def process_library_phone_number(message: types.Message, state: FSMContext):
    try:
        user_lang = await get_user_language(str(message.from_user.id))
        if not user_lang:
            user_lang = Language.EN

        user_data = await state.get_data()
        username = user_data["username"]
        password = user_data["password"]
        phone_number = message.text
        user_id = str(message.from_user.id)

        encrypted_password = encrypt_password(password)
        secret = await get_secret_key("0" + username)
        auth_key = await library_login(username, phone_number, password, secret)
        if not auth_key:
            await message.answer(Strings.get("library_login_failed", user_lang))
            return

        if await save_library_user(user_id, username, encrypted_password, phone_number):
            await message.answer(
                Strings.get("library_registration_successful", user_lang)
            )
            logging.info(f"User {user_id} registered in library successfully")
        else:
            await message.answer(Strings.get("failed_to_save_credentials", user_lang))
    except Exception as e:
        logging.error(f"Error in process_library_phone_number: {e}")
        await message.answer(Strings.get("unexpected_error", user_lang))
    finally:
        await message.delete()
        await state.clear()


def register_handlers(dp: Dispatcher):
    # Command handlers
    dp.message.register(cmd_register, Command("register"))
    dp.message.register(cmd_unregister, Command("unregister"))
    dp.message.register(cmd_library_register, Command("lregister"))

    # State handlers
    dp.message.register(process_username, RegistrationStates.waiting_for_username)
    dp.message.register(process_password, RegistrationStates.waiting_for_password)
    dp.message.register(
        process_library_username, LibraryRegistrationStates.waiting_for_username
    )
    dp.message.register(
        process_library_password, LibraryRegistrationStates.waiting_for_password
    )
    dp.message.register(
        process_library_phone_number, LibraryRegistrationStates.waiting_for_phone_number
    )
