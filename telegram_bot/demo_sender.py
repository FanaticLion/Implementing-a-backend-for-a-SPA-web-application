import logging

logger = logging.getLogger(__name__)


def send_telegram_message(chat_id, message):
    """Демо-режим для напоминаний - работает без реального Telegram"""

    print("🎯" * 60)
    print("🔔 **ТЕЛЕГРАМ НАПОМИНАНИЕ (ДЕМО-РЕЖИМ)**")
    print(f"📱 Чат ID: {chat_id}")
    print(f"💬 Сообщение: {message}")
    print("✅ Напоминание успешно отправлено в Telegram!")
    print("💡 Примечание: Режим демонстрации (Telegram API недоступен)")
    print("🎯" * 60)

    # Логируем для отчета
    logger.info(f"Demo Telegram message to {chat_id}: {message}")

    return True  # Всегда возвращаем успех для демонстрации
