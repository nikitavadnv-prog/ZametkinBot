from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Bot
from database import get_upcoming_trainings
import asyncio

def send_notification(bot: Bot, chat_id, message):
    try:
        bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print(f"Ошибка отправки: {e}")

def check_trainings(bot: Bot):
    from datetime import datetime, timedelta
    now = datetime.now()
    trainings = get_upcoming_trainings()
    for t in trainings:
        _, name, chat_id, dt_str = t
        training_time = datetime.strptime(dt_str, "%d.%m.%Y %H:%M")
        if training_time - timedelta(hours=24) <= now < training_time - timedelta(hours=23):
            send_notification(bot, chat_id, f"Напоминание: у вас тренировка завтра в {dt_str}")
        elif training_time - timedelta(hours=2) <= now < training_time - timedelta(hours=1):
            send_notification(bot, chat_id, f"Напоминание: у вас тренировка через 2 часа ({dt_str})")

def start_notifications(bot: Bot):
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_trainings, 'interval', minutes=10, args=(bot,))
    scheduler.start()
