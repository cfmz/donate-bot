import logging
import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8656680985:AAGh8ng_-xjIGcBkmdF5voLOB0aOSnEVvPY"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.process_update(update)
    return "OK", 200

@app.route("/")
def home():
    return "Бот работает!", 200

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Поддержать меня 👇\n______________________\n✅ Хороший гарант: @wozsk"
    keyboard = [
        [InlineKeyboardButton("1 ⭐", callback_data='1')],
        [InlineKeyboardButton("15 ⭐", callback_data='15'), InlineKeyboardButton("25 ⭐", callback_data='25')],
        [InlineKeyboardButton("50 ⭐", callback_data='50'), InlineKeyboardButton("100 ⭐", callback_data='100')]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    amount = int(query.data)

    await context.bot.send_invoice(
        chat_id=query.message.chat_id,
        title="Чаевые 👇",
        description="Поддержать меня",
        payload="donate",
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label="Чаевые", amount=amount)]
    )

application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button_click))

if __name__ == "__main__":
    RENDER_URL = "https://donate-bot-7iyd.onrender.com"
    application.bot.set_webhook(url=f"{RENDER_URL}/webhook")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
