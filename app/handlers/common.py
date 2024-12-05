import logging
from app.bot import bot
from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

from app.strings import Strings, Language
from app.services.llm import generate_response


async def cmd_start(message: types.Message):
    # Detect user's language from message.from_user.language_code
    # user_lang = (
    #     Language(message.from_user.language_code)
    #     if message.from_user.language_code in [l.value for l in Language]
    #     else Language.EN
    # )

    try:
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
        await message.answer(Strings.get("unexpected_error", Language.EN))


async def cmd_donate(message: types.Message):
    try:
        await message.reply_invoice(
            title="Buy me a coffee!😁",
            description="Thank you for using my bot!",
            prices=[types.LabeledPrice(label="Donation", amount=1)],
            currency="XTR",
            payload="donate",
            provider_token="",
        )
        logging.info(f"User {message.from_user.id} started donation")
    except Exception as e:
        logging.error(f"Error in cmd_donate: {e}")
        await message.answer(Strings.get("unexpected_error", Language.EN))


async def cmd_refund(message: types.Message):
    try:
        # Check if the message is a reply to a payment message
        if (
            not message.reply_to_message
            or not message.reply_to_message.successful_payment
        ):
            await message.answer(
                "Please reply to a payment message to request a refund!"
            )
            return

        payment = message.reply_to_message.successful_payment

        # Attempt to refund the payment
        result = await bot.refund_star_payment(
            user_id=message.from_user.id,
            telegram_payment_charge_id=payment.telegram_payment_charge_id,
        )

        if result:
            await message.answer("✅ Refund has been processed successfully.")
        else:
            await message.answer(
                "❌ Refund request was not successful. Please try again later."
            )

    except Exception as e:
        logging.error(f"Error in cmd_refund: {e}")
        await message.answer(Strings.get("unexpected_error", Language.EN))


async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    try:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    except Exception as e:
        logging.error(f"Error in process_pre_checkout_query: {e}")


# Process all other messages using LLM
async def other_message(message: types.Message):
    try:
        if message.content_type == types.ContentType.SUCCESSFUL_PAYMENT:
            await message.answer("Thank you for your donation!")

        elif message.content_type == types.ContentType.REFUNDED_PAYMENT:
            await message.answer(
                "Your payment has been refunded. Please contact the support if you have any questions."
            )

        elif message.text.startswith("/"):
            await message.reply(
                "This command is not available in the chat. Please use the command from the bot menu."
            )

        else:
            await message.reply(await generate_response(message.text))
            logging.info(f"User {message.from_user.id} asked a question (LLM)")

    except Exception as e:
        logging.error(f"Error in other_message: {e}")
        await message.answer(Strings.get("unexpected_error", Language.EN))


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_donate, Command("donate"))
    dp.message.register(cmd_refund, Command("refund"))
    dp.pre_checkout_query.register(process_pre_checkout_query)
    dp.message.register(other_message)
