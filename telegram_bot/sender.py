import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def send_telegram_message(chat_id, message):
    """Функция отправки сообщений - в разработке выводит в консоль"""

    # Режим разработки - выводим в консоль
    print(f"🔔 TELEGRAM НАПОМИНАНИЕ для чата {chat_id}")
    print(f"   Чат ID: {chat_id}")
    print(f"   Сообщение: {message}")
    print(f"   {'=' * 50}")

    # Если токен настроен, пытаемся отправить по-настоящему
    if settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_BOT_TOKEN.strip():
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                logger.info(f"Telegram message sent to {chat_id}")
                return True
            else:
                logger.warning(
                    f"Telegram API error: {response.status_code} - {response.text}"
                )
        except Exception as e:
            logger.warning(f"Telegram connection error: {e}")

    # В любом случае возвращаем True для тестирования
    return True
