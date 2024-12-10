import pytest
from unittest.mock import AsyncMock, patch, create_autospec
from aiogram import types

from app.handlers.common import cmd_start, cmd_language
from app.handlers.auth import cmd_register
from app.strings import Language


@pytest.mark.asyncio
async def test_cmd_start():
    # Create proper mock objects
    from_user = AsyncMock()
    from_user.id = "789"
    from_user.first_name = "Test User"

    message = AsyncMock(spec=types.Message)
    message.from_user = from_user
    message.reply_photo = AsyncMock()

    with patch("app.database.database.get_user_language", return_value=None):
        await cmd_start(message)

    message.reply_photo.assert_called_once()


@pytest.mark.asyncio
async def test_cmd_language():
    # Create proper mock objects
    from_user = AsyncMock()
    from_user.id = "test123"

    message = AsyncMock(spec=types.Message)
    message.from_user = from_user
    message.answer = AsyncMock()

    with patch("app.database.database.get_user_language", return_value=Language.EN):
        await cmd_language(message)

    message.answer.assert_called_once()
    assert "/register" in message.answer.call_args[0][0]
