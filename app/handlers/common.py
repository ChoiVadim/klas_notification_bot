from app.bot import bot
from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

from app.services.llm import generate_response


async def cmd_start(message: types.Message):
    caption = f"""Welcome, {message.from_user.first_name}!👋
This bot is made for the students of Kwangwoon University 🏫
This bot will track your all assignments and notify you when they are less than 24 hours left 🧭

/register to start registration
/unregister to delete all your information from the bot
/show If you want to see all your tasks to do 🔍
/info If you want to see your graduation information 📝

❗ You need to register to use main features. This bot will encrypt your password and username. I do not save your credentials in visible form. So don't worry about your privacy.
I would appreciate if you could help me to improve this bot.
Send me any feedback or suggestions to @tsoivadim 💬
And i will try to improve this bot as soon as possible!

Made with ❤️ by @tsoivadim
"""
    photo = FSInputFile("images/logo.jpg")
    await message.reply_photo(
        photo=photo,
        caption=caption,
    )


async def cmd_donate(message: types.Message):
    await message.reply_invoice(
        title="Buy me a coffee!😁",
        description="Thank you for using my bot!",
        prices=[types.LabeledPrice(label="Donation", amount=1)],
        currency="XTR",
        payload="donate",
        provider_token="",
    )


async def cmd_refund(message: types.Message):
    try:
        # Check if the message is a reply to a payment message
        if (
            not message.reply_to_message
            or not message.reply_to_message.successful_payment
        ):
            await message.answer(
                "Please reply to a payment message to request a refund."
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
        await message.answer(f"❌ Error processing refund: {str(e)}")


async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def other_message(message: types.Message):
    if message.content_type == types.ContentType.SUCCESSFUL_PAYMENT:
        await message.answer("Thank you for your donation!")
    else:
        await bot.send_message(
            message.from_user.id, await generate_response(message.text)
        )


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_donate, Command("donate"))
    dp.message.register(cmd_refund, Command("refund"))
    dp.pre_checkout_query.register(process_pre_checkout_query)
    dp.message.register(other_message)
