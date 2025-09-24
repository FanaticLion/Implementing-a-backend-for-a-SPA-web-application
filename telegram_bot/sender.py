import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def send_telegram_message(chat_id, message):
    """Отправка сообщения через Telegram Bot API"""
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.error("Telegram bot token not configured")
        return False

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        logger.info(f"Message sent to chat_id {chat_id}")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending Telegram message to {chat_id}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False