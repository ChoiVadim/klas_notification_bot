import logging
from aiogram import Dispatcher, types
from aiogram.filters import Command
from typing import Optional

from app.config import settings
from app.database.database import get_all_users
from app.strings import Strings, Language


async def cmd_notify(message: types.Message):
    try:
        # Check if the user is an admin
        if message.from_user.id != settings.ADMIN_ID:
            await message.answer("You are not authorized to use this command.")
            return

        # Parse the message format: /notify en: English message | ko: 한국어 메시지
        content = message.text.split("/notify ", 1)[1] if not message.photo else message.caption.split("/notify ", 1)[1]
        
        # Parse messages for different languages
        messages = parse_multilanguage_message(content)
        
        if not messages:
            await message.answer("Please use the format:\n/notify en: English message | ko: 한국어 메시지")
            return

        # Fetch all users from the database
        users = await get_all_users()

        if message.photo:
            photo = message.photo[-1].file_id
            for user in users:
                try:
                    # Get user's preferred language (default to English if not set)
                    user_lang = getattr(user, 'language', 'en')
                    caption = messages.get(user_lang, messages.get('en', ''))
                    
                    await message.bot.send_photo(
                        chat_id=user.user_id,
                        photo=photo,
                        caption=caption
                    )
                except Exception as e:
                    logging.error(f"Failed to send message to {user.user_id}: {e}")
        else:
            for user in users:
                try:
                    # Get user's preferred language (default to English if not set)
                    user_lang = getattr(user, 'language', 'en')
                    msg = messages.get(user_lang, messages.get('en', ''))
                    
                    await message.bot.send_message(
                        chat_id=user.user_id,
                        text=msg
                    )
                except Exception as e:
                    logging.error(f"Failed to send message to {user.user_id}: {e}")

        await message.answer("Notification sent to all users!")

    except Exception as e:
        logging.error(f"Failed to send notification: {e}")
        await message.answer(Strings.get("unexpected_error", Language.EN))


def parse_multilanguage_message(content: str) -> dict[str, str]:
    """
    Parse a message with multiple language versions
    Format: en: English message | ko: 한국어 메시지
    """
    try:
        messages = {}
        parts = content.split('|')
        
        for part in parts:
            part = part.strip()
            if ':' in part:
                lang, msg = part.split(':', 1)
                lang = lang.strip().lower()
                msg = msg.strip()
                messages[lang] = msg
                
        return messages
    except Exception as e:
        logging.error(f"Error parsing multilanguage message: {e}")
        return {}


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_notify, Command("notify"))
