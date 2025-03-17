import time
import logging

from aiogram.types import Message
from aiogram import BaseMiddleware

from app.strings import Strings
from app.utils.language_utils import get_user_language_with_fallback


class AntiSpamMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 2):
        super().__init__()
        self.limit = limit
        self.user_last_message_time = {}

    async def __call__(self, handler, event: Message, data: dict):
        try:
            user_id = event.from_user.id
            current_time = time.time()
            user_lang = await get_user_language_with_fallback(event)

            # Check if the user has sent a message recently
            if user_id in self.user_last_message_time:
                last_message_time = self.user_last_message_time[user_id]
                if current_time - last_message_time < self.limit:
                    await event.answer(Strings.get("too_many_messages", user_lang))
                    return

            # Update the last message time
            self.user_last_message_time[user_id] = current_time

            # Proceed with the next handler
            return await handler(event, data)
        except Exception as e:
            logging.error(f"Error in AntiSpamMiddleware: {e}")
            return await handler(event, data)
