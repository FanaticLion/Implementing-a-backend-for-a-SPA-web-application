import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Проверим что Django настроен
try:
    from django.conf import settings
except ImportError:
    print("Django not configured")
    exit(1)

logger = logging.getLogger(__name__)


class HabitTrackerBot:
    def __init__(self):
        # Проверяем что токен есть в настройках
        if not hasattr(settings, 'TELEGRAM_BOT_TOKEN') or not settings.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN not configured in Django settings")

        self.token = settings.TELEGRAM_BOT_TOKEN
        self.application = None

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user
        chat_id = update.effective_chat.id

        await update.message.reply_text(
            f"Привет, {user.first_name}! 👋\n\n"
            f"🤖 Я бот для напоминаний о привычках!\n\n"
            f"Твой chat_id: `{chat_id}`\n\n"
            f"📝 Используй этот chat_id в своем профиле на сайте, "
            f"чтобы получать уведомления о привычках.\n\n"
            f"Команды:\n"
            f"/help - показать справку\n"
            f"/myid - показать твой chat_id",
            parse_mode='Markdown'
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        await update.message.reply_text(
            "🤖 Habit Tracker Bot\n\n"
            "Я помогу тебе не забывать о твоих привычках!\n\n"
            "📋 Команды:\n"
            "/start - начать работу\n"
            "/help - эта справка\n"
            "/myid - показать твой chat_id\n\n"
            "🔔 Для получения уведомлений:\n"
            "1. Скопируй свой chat_id командой /myid\n"
            "2. Войди на сайт habit tracker\n"
            "3. Укажи chat_id в профиле\n"
            "4. Настрой привычки с временем выполнения\n"
            "5. Получай уведомления вовремя! 🎯"
        )

    async def myid_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать chat_id пользователя"""
        chat_id = update.effective_chat.id
        await update.message.reply_text(
            f"Твой chat_id: `{chat_id}`\n\n"
            f"Скопируй этот номер и укажи его в своем профиле на сайте.",
            parse_mode='Markdown'
        )

    def setup_handlers(self):
        """Настройка обработчиков команд"""
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("myid", self.myid_command))

    async def run_polling(self):
        """Запуск бота в режиме polling"""
        if not self.token:
            logger.error("Telegram bot token not set")
            return

        # Создаем приложение
        self.application = Application.builder().token(self.token).build()

        # Настраиваем обработчики
        self.setup_handlers()

        logger.info("Telegram бот запущен в режиме polling...")

        # Запускаем бота
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()

        # Бесконечный цикл
        await asyncio.Event().wait()

    async def stop(self):
        """Остановка бота"""
        if self.application:
            await self.application.stop()


async def main():
    """Основная функция"""
    bot = HabitTrackerBot()
    try:
        await bot.run_polling()
    except KeyboardInterrupt:
        await bot.stop()


def run_bot():
    """Функция для запуска бота"""
    asyncio.run(main())