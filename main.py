import asyncio
import logging
from app.bot import dp, bot, setup_handlers
from app.database.database import init_db
from app.services.notifications import start_notification_service


async def main():
    logging.info("Starting bot...")

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
        logging.info("Closing bot session")
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        encoding="UTF-8",
    )
    asyncio.run(main())
