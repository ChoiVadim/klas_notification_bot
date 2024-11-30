import time
from aiogram.types import Message
from aiogram import BaseMiddleware


class AntiSpamMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 2):
        super().__init__()
        self.limit = limit
        self.user_last_message_time = {}

    async def __call__(self, handler, event: Message, data: dict):
        user_id = event.from_user.id
        current_time = time.time()

        # Check if the user has sent a message recently
        if user_id in self.user_last_message_time:
            last_message_time = self.user_last_message_time[user_id]
            if current_time - last_message_time < self.limit:
                await event.answer(
                    "You are sending messages too quickly. Please wait a moment."
                )
                return

        # Update the last message time
        self.user_last_message_time[user_id] = current_time

        # Proceed with the next handler
        return await handler(event, data)
