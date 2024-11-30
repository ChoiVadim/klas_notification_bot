import asyncio
import logging
from app.bot import dp, bot, setup_handlers
from app.database.database import init_db
from app.services.notifications import check_todos


async def main():
    logging.info("Starting bot...")
    await init_db()

    # Setup all handlers
    setup_handlers(dp)

    # Start polling and notifications
    await asyncio.gather(dp.start_polling(bot), check_todos())


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename="log.txt",
        filemode="a",
        encoding="UTF-8",
    )
    asyncio.run(main())
