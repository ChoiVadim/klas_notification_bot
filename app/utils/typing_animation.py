import asyncio
import logging
from app.bot import bot


class show_typing_action:
    """Context manager for showing typing action while processing a response"""

    def __init__(self, chat_id, action="typing", interval=4.0):
        self.chat_id = chat_id
        self.action = action
        self.interval = interval
        self.task = None

    async def __aenter__(self):
        # Start sending typing action periodically
        self.task = asyncio.create_task(self._send_action_periodically())
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Cancel the periodic task when exiting context
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass

    async def _send_action_periodically(self):
        """Sends typing action every few seconds to keep the indicator active"""
        try:
            while True:
                await bot.send_chat_action(self.chat_id, self.action)
                await asyncio.sleep(self.interval)
        except asyncio.CancelledError:
            # Expected when the context manager exits
            pass
        except Exception as e:
            logging.error(f"Error sending chat action: {e}")
