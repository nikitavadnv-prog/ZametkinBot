from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from database import init_db, add_training
from notifications import start_notifications
import config

# Инициализация базы данных
init_db()

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я бот для записи на тренировки. Используй /add для добавления клиента.")

def add_client(update: Update, context: CallbackContext):
    update.message.reply_text("Введите имя клиента, дату и время тренировки в формате:\nИмя 01.01.2025 15:00")

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    try:
        parts = text.split()
        name = parts[0]
        date_time = f"{parts[1]} {parts[2]}"
        chat_id = update.message.chat_id
        add_training(name, chat_id, date_time)
        update.message.reply_text(f"Клиент {name} записан на {date_time}")
    except:
        update.message.reply_text("Ошибка формата. Попробуйте снова.")

# Создаем обработчики
updater = Updater(token=config.TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("add", add_client))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Запуск уведомлений (после создания бота)
start_notifications(updater.bot)

# Запуск бота
if __name__ == '__main__':
    updater.start_polling()
    updater.idle()
