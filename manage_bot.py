import os

import django

from telegram_bot.bot import run_bot

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django.setup()

if __name__ == "__main__":
    run_bot()
