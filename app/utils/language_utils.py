from aiogram import types
from app.strings import Language
from app.database.database import get_user_language

async def get_user_language_with_fallback(user, user_id=None):
    """
    Gets the user's language with fallback to their client language.
    
    Args:
        user: Either a Message object, CallbackQuery object, or User object with a from_user attribute
        user_id: Optional user ID string if not using a Message or CallbackQuery object
        
    Returns:
        Language enum value
    """
    # If we received a Message or CallbackQuery object, extract the user
    if hasattr(user, 'from_user'):
        user_obj = user.from_user
        if not user_id:
            user_id = str(user_obj.id)
    else:
        user_obj = user
        
    # First try to get language from database
    user_lang = await get_user_language(user_id)
    
    # If not found in database, use client language or fallback to English
    if not user_lang:
        language_code_map = {"en": "EN", "ko": "KO", "ru": "RU"}
        if hasattr(user_obj, 'language_code') and user_obj.language_code in language_code_map:
            mapped_code = language_code_map[user_obj.language_code]
            user_lang = Language[mapped_code]
        else:
            user_lang = Language.EN
            
    return user_lang
