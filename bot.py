cat > bot.py << 'EOF'
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8669610102:AAH59AUn8lEXOvLzX6b2-kxitcWYMmtl9Tw"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Поддержать меня 👇\n______\n✅ Хороший гарант: @wozsk"
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

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))
    print("✅ Бот запущен! Нажми /start в Telegram.")
    application.run_polling()

if name == "main":
    main()
EOF

pip install python-telegram-bot && python bot.py
