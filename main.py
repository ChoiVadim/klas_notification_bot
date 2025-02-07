import asyncio
import logging
from app.bot import dp, bot, setup_handlers
from app.database.database import init_db
from app.services.notifications import start_notification_service
from app.config import settings
from app.menu import initialize_bot_menu


async def main():
    await bot.send_message(chat_id=settings.ADMIN_ID, text="Bot started successfully!")
    await initialize_bot_menu()


    # Initialize database
    await init_db()

    # Setup all handlers
    setup_handlers(dp)

    # Create tasks for both the notification service and bot polling
    notification_task = asyncio.create_task(start_notification_service())
    polling_task = asyncio.create_task(dp.start_polling(bot))

    # Wait for both tasks to run
    try:
        await asyncio.gather(notification_task, polling_task)
    except Exception as e:
        logging.error(f"Error in main loop: {e}")
    finally:
        # Cleanup if needed
        await bot.send_message(
            chat_id=settings.ADMIN_ID, text="Bot is shutting down..."
        )
        await bot.session.close()


if __name__ == "__main__":
    import platform

    # Configure logging first
    if platform.system() == "Linux":
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            filename="/var/log/kwbot.log",
            filemode="a",
            encoding="UTF-8",
        )
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    logging.info("Starting bot...")
    asyncio.run(main())
    logging.info("Program finished!")
