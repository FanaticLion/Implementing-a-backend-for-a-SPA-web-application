#!/usr/bin/env python
import os
import django

# Настраиваем Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

# Инициализируем Django
django.setup()

# Теперь импортируем бота после настройки Django
from telegram_bot.bot import run_bot

if __name__ == '__main__':
    print("Starting Telegram bot...")
    run_bot()