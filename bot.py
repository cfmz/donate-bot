import logging
import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Токен вашего бота
TOKEN = "8807622473:AAHPkinQOlUEKvnJ27HRHXvUDXPk_6T945w"

# Настройка логирования
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Создаем Flask приложение (для ответа Render)
app = Flask(__name__)

# Создаем Telegram приложение
application = Application.builder().token(TOKEN).build()

# Точка входа для вебхуков от Telegram
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.process_update(update)
    return "OK", 200

# Проверка, что сервер жив
@app.route("/")
def home():
    return "Бот работает!", 200

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Поддержать меня 👇\n______________________\n✅ Хороший гарант: @wozsk"
    keyboard = [
        [InlineKeyboardButton("1 ⭐", callback_data='1')],
        [InlineKeyboardButton("15 ⭐", callback_data='15'), InlineKeyboardButton("25 ⭐", callback_data='25')],
        [InlineKeyboardButton("50 ⭐", callback_data='50'), InlineKeyboardButton("100 ⭐", callback_data='100')]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# Обработка нажатий на кнопки
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    amount = int(query.data)

    # Выставление счета в Звездах (без провайдера)
    await context.bot.send_invoice(
        chat_id=query.message.chat_id,
        title="Чаевые 👇",
        description="Поддержать меня",
        payload="donate",
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label="Чаевые", amount=amount)]
    )

# Добавляем обработчики в приложение
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button_click))

# Точка запуска
if __name__ == "__main__":
    # Получаем URL вашего приложения на Render
    # В Render есть переменная окружения RENDER_EXTERNAL_URL, но надежнее вписать вручную:
    RENDER_URL = "https://YOUR_APP_NAME.onrender.com" # <--- ОБЯЗАТЕЛЬНО ЗАМЕНИТЕ НА СВОЙ URL
    
    # Устанавливаем вебхук
    application.bot.set_webhook(url=f"{RENDER_URL}/webhook")
    
    # Запускаем Flask сервер
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
