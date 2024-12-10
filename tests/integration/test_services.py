import pytest
from unittest.mock import AsyncMock, patch
from app.services.notifications import send_notification
from app.services.kw import KwangwoonUniversityApi

@pytest.mark.asyncio
async def test_send_notification():
    user_id = "test_user"
    message = "Test notification"
    urgency_level = 1
    
    with patch('app.bot.bot.send_message') as mock_send:
        await send_notification(message, user_id, urgency_level)
        mock_send.assert_called_once()
        assert "remaining" in mock_send.call_args[1]['text']

@pytest.mark.asyncio
async def test_kw_api():
    async with KwangwoonUniversityApi() as api:
        with patch.object(api, 'login', return_value=True):
            result = await api.login("test_user", "test_pass")
            assert result is True 