# import pytest
# from unittest.mock import AsyncMock, patch
# from aiogram import types
# from app.bot import dp, setup_handlers
# from app.database.database import init_db, save_user
# from app.utils.encryption import encrypt_password
# from app.strings import Language


# @pytest.fixture(scope="function")
# async def setup_bot(event_loop):
#     await init_db()
#     setup_handlers(dp)
#     return dp


# @pytest.mark.asyncio
# async def test_full_registration_flow(setup_bot):
#     from_user = AsyncMock()
#     from_user.id = "test_user_id"
#     from_user.first_name = "Test User"

#     register_message = AsyncMock(spec=types.Message)
#     register_message.from_user = from_user
#     register_message.text = "/register"

#     username_message = AsyncMock(spec=types.Message)
#     username_message.from_user = from_user
#     username_message.text = "test_username"

#     password_message = AsyncMock(spec=types.Message)
#     password_message.from_user = from_user
#     password_message.text = "test_password"

#     with patch("app.services.kw.KwangwoonUniversityApi") as mock_kw:
#         mock_instance = AsyncMock()
#         mock_instance.login.return_value = True
#         mock_kw.return_value.__aenter__.return_value = mock_instance

#         register_handler = next(
#             h.handler
#             for h in setup_bot.message.handlers
#             if "/register" in str(h.filters)
#         )
#         username_handler = next(
#             h.handler
#             for h in setup_bot.message.handlers
#             if "username" in str(h.filters)
#         )
#         password_handler = next(
#             h.handler
#             for h in setup_bot.message.handlers
#             if "password" in str(h.filters)
#         )

#         await register_handler(register_message)
#         register_message.answer.assert_called_once()

#         await username_handler(username_message)
#         username_message.answer.assert_called_once()

#         await password_handler(password_message)
#         password_message.answer.assert_called_once()


# @pytest.mark.asyncio
# async def test_language_change_flow(setup_bot):
#     user_id = "lang_test_user"
#     await save_user(user_id, "testuser", encrypt_password("testpass"))

#     from_user = AsyncMock()
#     from_user.id = user_id

#     callback_query = AsyncMock(spec=types.CallbackQuery)
#     callback_query.from_user = from_user
#     callback_query.data = "language_ko"
#     callback_query.message = AsyncMock()

#     language_handler = next(
#         h.handler
#         for h in setup_bot.callback_query.handlers
#         if "language" in str(h.filters)
#     )
#     await language_handler(callback_query)
#     callback_query.message.edit_text.assert_called_once()


# @pytest.mark.asyncio
# async def test_todo_list_flow(setup_bot):
#     user_id = "todo_test_user"
#     await save_user(user_id, "todouser", encrypt_password("todopass"))

#     from_user = AsyncMock()
#     from_user.id = user_id

#     todo_message = AsyncMock(spec=types.Message)
#     todo_message.from_user = from_user
#     todo_message.text = "/todos"

#     mock_todos = {
#         "name": "Test Subject",
#         "todo": {
#             "lectures": [{"title": "Test Lecture", "left_time": "2 days"}],
#             "homeworks": [{"title": "Test Homework", "left_time": "1 day"}],
#         },
#     }

#     with patch("app.services.kw.KwangwoonUniversityApi") as mock_kw:
#         mock_instance = AsyncMock()
#         mock_instance.get_todo_list.return_value = [mock_todos]
#         mock_kw.return_value.__aenter__.return_value = mock_instance

#         todos_handler = next(
#             h.handler for h in setup_bot.message.handlers if "/todos" in str(h.filters)
#         )
#         await todos_handler(todo_message)
#         todo_message.answer.assert_called_once()


# @pytest.mark.asyncio
# async def test_error_handling(setup_bot):
#     from_user = AsyncMock()
#     from_user.id = "error_test_user"

#     invalid_message = AsyncMock(spec=types.Message)
#     invalid_message.from_user = from_user
#     invalid_message.text = "/invalidcommand"

#     error_handler = next(
#         h.handler
#         for h in setup_bot.message.handlers
#         if getattr(h, "is_error_handler", False)
#     )
#     await error_handler(invalid_message)
#     invalid_message.answer.assert_called_once()

#     invalid_message.answer.assert_called_once()
