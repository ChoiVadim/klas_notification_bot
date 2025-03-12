import logging

from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

from app.bot import bot
from app.strings import Strings, Language
from app.services.llm import generate_response
from app.keyboards import create_language_keyboard
from app.database.database import get_user_language
from app.utils.typing_animation import show_typing_action
from app.utils.chat_history import get_chat_history, store_message_in_history


async def cmd_start(message: types.Message):
    try:
        user_lang = await get_user_language(str(message.from_user.id))

        if not user_lang:
            if message.from_user.language_code in ["ko", "ru", "en"]:
                user_lang = Language(message.from_user.language_code)
            else:
                user_lang = Language.EN

        caption = Strings.get("welcome", user_lang, name=message.from_user.first_name)
        photo = FSInputFile("images/logo.jpg")
        await message.reply_photo(
            photo=photo,
            caption=caption,
        )
        logging.info(f"User {message.from_user.id} started the bot!")
    except Exception as e:
        logging.error(f"Error in cmd_start: {e}")
        await message.answer(Strings.get("unexpected_error", user_lang))


async def cmd_language(message: types.Message):
    try:
        status = await get_user_language(str(message.from_user.id))
        if not status:
            await message.answer(
                Strings.get("language_change_failed", Language.EN),
            )

        else:
            await message.answer(
                "🇺🇸 Choose your language\n🇰🇷 언어 선택\n🇷🇺 Выберите язык",
                reply_markup=create_language_keyboard(),
            )
    except Exception as e:
        logging.error(f"Error in cmd_language: {e}")


async def cmd_donate(message: types.Message):
    try:
        user_lang = await get_user_language(str(message.from_user.id))
        if not user_lang:
            user_lang = Language.EN

        await message.reply_invoice(
            title=Strings.get("donate_title", user_lang),
            description=Strings.get("donate_description", user_lang),
            prices=[types.LabeledPrice(label="Donation", amount=1)],
            currency="XTR",
            payload="donate",
            provider_token="",
        )
        logging.info(f"User {message.from_user.id} started donation")
    except Exception as e:
        logging.error(f"Error in cmd_donate: {e}")
        await message.answer(Strings.get("unexpected_error", user_lang))


async def cmd_refund(message: types.Message):
    try:
        user_lang = await get_user_language(str(message.from_user.id))
        if not user_lang:
            user_lang = Language.EN

        # Check if the message is a reply to a payment message
        if (
            not message.reply_to_message
            or not message.reply_to_message.successful_payment
        ):
            await message.answer(Strings.get("refund_error", user_lang))
            return

        payment = message.reply_to_message.successful_payment

        # Attempt to refund the payment
        result = await bot.refund_star_payment(
            user_id=message.from_user.id,
            telegram_payment_charge_id=payment.telegram_payment_charge_id,
        )

        if result:
            await message.answer(Strings.get("refund_success", user_lang))
        else:
            await message.answer(Strings.get("refund_error", user_lang))

    except Exception as e:
        logging.error(f"Error in cmd_refund: {e}")
        await message.answer(Strings.get("unexpected_error", user_lang))


async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    try:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    except Exception as e:
        logging.error(f"Error in process_pre_checkout_query: {e}")


# TODO: Add voice support and handle other content types
async def other_message(message: types.Message):
    try:
        user_lang = await get_user_language(str(message.from_user.id))
        if not user_lang:
            user_lang = Language.EN

        if message.content_type == types.ContentType.SUCCESSFUL_PAYMENT:
            await message.answer(Strings.get("successful_payment", user_lang))

        elif message.content_type == types.ContentType.REFUNDED_PAYMENT:
            pass

        elif message.content_type == types.ContentType.PHOTO:
            await message.reply(
                "Photo is not available in the chat. Please use the command from the bot menu."
            )
        elif message.content_type == types.ContentType.DOCUMENT:
            await message.reply(
                "Document is not available in the chat. Please use the command from the bot menu."
            )
        elif message.content_type == types.ContentType.AUDIO:
            await message.reply(
                "Audio is not available in the chat. Please use the command from the bot menu."
            )
        elif (
            message.content_type == types.ContentType.VIDEO
            or message.content_type == types.ContentType.VIDEO_NOTE
        ):
            await message.reply(
                "Video is not available in the chat. Please use the command from the bot menu."
            )
        elif message.content_type == types.ContentType.VOICE:
            # TODO: Add voice support
            await message.reply(
                "Voice is not available in the chat. Please use the command from the bot menu."
            )
        elif (
            message.content_type == types.ContentType.STICKER
            or message.content_type == types.ContentType.ANIMATION
        ):
            await message.reply(
                "Sticker and GIF is not available in the chat. Please use the command from the bot menu."
            )
        elif message.content_type == types.ContentType.LOCATION:
            await message.reply(
                "Location is not available in the chat. Please use the command from the bot menu."
            )
        elif message.text.startswith("/"):
            await message.reply(
                "This command is not available in the chat. Please use the command from the bot menu."
            )
        else:
            # Get previous messages
            previous_messages = get_chat_history(message.chat.id)

            # Start "typing" action to show the bot is processing
            async with show_typing_action(message.chat.id):
                response = await generate_response(message.text, previous_messages)

                # Store messages in history
                store_message_in_history(message.chat.id, message.text, "user")
                store_message_in_history(message.chat.id, response, "assistant")

            # Send the response after typing is complete
            await message.reply(response, parse_mode="MarkdownV2")
            logging.info(f"User {message.from_user.id} asked a question (LLM)")

    except Exception as e:
        logging.error(f"Error in other_message: {e}")
        await message.answer(Strings.get("unexpected_error", user_lang))


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_donate, Command("donate"))
    dp.message.register(cmd_refund, Command("refund"))
    dp.message.register(cmd_language, Command("language"))
    dp.pre_checkout_query.register(process_pre_checkout_query)
    dp.message.register(other_message)
