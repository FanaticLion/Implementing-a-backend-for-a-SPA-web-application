import os
import time

import django
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django.setup()

TOKEN = "8154524781:AAEK51BW5y869597ZFqk1TAkrrvH6_VuTho"


def simple_polling_bot():
    print("🤖 Запускаю простого Telegram бота...")

    # Проверим токен
    response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getMe")
    print("Токен:", response.json())

    last_update_id = 0

    while True:
        try:
            # Получаем новые сообщения
            response = requests.get(
                f"https://api.telegram.org/bot{TOKEN}/getUpdates",
                params={"offset": last_update_id + 1, "timeout": 30},
            )

            if response.status_code == 200:
                data = response.json()
                if data["ok"] and data["result"]:
                    for update in data["result"]:
                        last_update_id = update["update_id"]

                        if "message" in update:
                            message = update["message"]
                            chat_id = message["chat"]["id"]
                            text = message.get("text", "")

                            print(f"📨 Получено: '{text}' от {chat_id}")

                            # Обрабатываем команды
                            if text == "/start":
                                msg = f"✅ Бот работает! Твой chat_id: {chat_id}"
                                requests.post(
                                    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                                    json={"chat_id": chat_id, "text": msg},
                                )
                                print(f"📤 Отправил: {msg}")

                            elif text == "/myid":
                                msg = f"Твой chat_id: `{chat_id}`"
                                requests.post(
                                    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                                    json={
                                        "chat_id": chat_id,
                                        "text": msg,
                                        "parse_mode": "Markdown",
                                    },
                                )

            time.sleep(1)

        except Exception as e:
            print(f"❌ Ошибка: {e}")
            time.sleep(5)


if __name__ == "__main__":
    simple_polling_bot()
