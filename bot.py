import os
import uuid
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, PreCheckoutQueryHandler, MessageHandler, filters

TOKEN = os.environ.get("BOT_TOKEN")  # Безопасно берем из переменной окружения
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")  # Render сам подставит URL вашего сервиса

async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("1 ⭐", callback_data="1")],
        [InlineKeyboardButton("15 ⭐", callback_data="15"),
         InlineKeyboardButton("25 ⭐", callback_data="25")],
        [InlineKeyboardButton("50 ⭐", callback_data="50"),
         InlineKeyboardButton("100 ⭐", callback_data="100")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_text = (
        "Поддержать меня 👇\n"
        "______________________\n"
        "✅ Хороший гарант: @wozsk"
    )
    await update.message.reply_text(message_text, reply_markup=reply_markup)

async def button_callback(update: Update, context):
    query = update.callback_query
    await query.answer()
    amount = int(query.data)
    payload = str(uuid.uuid4())
    prices = [LabeledPrice(label="⭐", amount=amount)]
    await context.bot.send_invoice(
        chat_id=query.message.chat_id,
        title="Чаевые 👇",
        description="Поддержать меня",
        payload=payload,
        provider_token="",
        currency="XTR",
        prices=prices
    )

async def pre_checkout_callback(update: Update, context):
    query = update.pre_checkout_query
    await query.answer(ok=True)

async def successful_payment_callback(update: Update, context):
    await update.message.reply_text("Спасибо за поддержку! ❤️")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback, pattern="^(1|15|25|50|100)$"))
    app.add_handler(PreCheckoutQueryHandler(pre_checkout_callback))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))

    # Запуск вебхука
    app.run_webhook(
        listen="0.0.0.0",
        port=10000,  # Render обычно требует порт 10000
        webhook_url=f"{RENDER_URL}/webhook"
    )

if __name__ == "__main__":
    main()
