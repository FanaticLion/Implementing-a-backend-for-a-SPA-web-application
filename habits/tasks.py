import logging
from celery import shared_task
from django.utils import timezone
from habits.models import Habit
from telegram_bot.demo_sender import send_telegram_message

logger = logging.getLogger(__name__)


@shared_task
def send_habit_reminders():
    """Задача для отправки напоминаний о привычках"""
    now = timezone.now()
    current_time = now.time()

    logger.info(f"Checking habits for time: {current_time}")

    # Находим привычки, которые нужно выполнить сейчас
    habits = Habit.objects.filter(
        time__hour=current_time.hour, time__minute=current_time.minute
    )

    for habit in habits:
        if habit.user.telegram_chat_id:
            send_habit_reminder.delay(habit.id)
            logger.info(f"Scheduled reminder for habit: {habit.action}")


@shared_task
def send_habit_reminder(habit_id):
    """Отправка напоминания конкретной привычки"""
    try:
        habit = Habit.objects.get(id=habit_id)
        if habit.user.telegram_chat_id:
            message = (
                f"🔔 **Напоминание о привычке!**\n\n"
                f"**Привычка:** {habit.action}\n"
                f"**Место:** {habit.place}\n"
                f"**Время на выполнение:** {habit.time_to_complete} сек.\n\n"
            )

            if habit.reward:
                message += f"**Вознаграждение:** {habit.reward}\n\n"
            elif habit.related_habit:
                message += f"**Следующая привычка:** {habit.related_habit.action}\n\n"

            message += "Удачи! 💪"

            success = send_telegram_message(habit.user.telegram_chat_id, message)
            if success:
                logger.info(f"Reminder sent for habit: {habit.action}")
            else:
                logger.error(f"Failed to send reminder for habit: {habit.action}")

    except Habit.DoesNotExist:
        logger.error(f"Habit with id {habit_id} not found")
    except Exception as e:
        logger.error(f"Error sending reminder: {e}")
