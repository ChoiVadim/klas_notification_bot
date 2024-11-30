from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.config import settings
from app.middleware.antispam import AntiSpamMiddleware

storage = MemoryStorage()
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(storage=storage)

# Register the anti-spam middleware
dp.message.middleware(AntiSpamMiddleware(limit=2))


def setup_handlers(dp: Dispatcher):
    from app.handlers import auth, assignments, food, common, student_info, callbacks

    # Register all handlers
    auth.register_handlers(dp)
    assignments.register_handlers(dp)
    student_info.register_handlers(dp)
    food.register_handlers(dp)
    callbacks.register_handlers(dp)
    common.register_handlers(dp)
