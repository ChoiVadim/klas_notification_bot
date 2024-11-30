import logging
from aiogram import Dispatcher, types
from aiogram.filters import Command

from app.config import settings
from app.database.database import get_all_users


async def cmd_notify(message: types.Message):
    try:
        # Check if the user is an admin
        if message.from_user.id != settings.ADMIN_ID:
            await message.answer("You are not authorized to use this command.")
            return

        # Fetch all users from the database
        users = await get_all_users()

        if message.photo:
            # Extract the text and photo from the message
            photo = message.photo[-1].file_id  # Get the highest resolution photo
            caption = message.caption.split("/notify")[1]

            # Send the message and photo to each user
            for user in users:
                try:
                    await message.bot.send_photo(
                        chat_id=user.user_id, photo=photo, caption=caption
                    )
                except Exception as e:
                    logging.error(f"Failed to send message to {user.user_id}: {e}")

            await message.answer("Notification sent to all users!")
        else:
            msg = " ".join(message.text.split(" ")[1:])
            for user in users:
                try:
                    await message.bot.send_message(chat_id=user.user_id, text=msg)
                except Exception as e:
                    logging.error(f"Failed to send message to {user.user_id}: {e}")

    except Exception as e:
        logging.error(f"Failed to send notification: {e}")


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_notify, Command("notify"))
