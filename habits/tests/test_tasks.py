from unittest.mock import patch

from django.test import TestCase

from habits.models import Habit
from habits.tasks import send_habit_reminder
from users.models import User


class TasksTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            telegram_chat_id="12345",
        )
        self.habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="12:00:00",
            action="Тест привычка",
            time_to_complete=60,
        )

    @patch("habits.tasks.send_telegram_message")
    def test_send_habit_reminder(self, mock_send):
        """Тест отправки напоминания"""
        mock_send.return_value = True

        # Вызываем задачу напрямую (не через delay)
        send_habit_reminder(self.habit.id)

        # Проверяем, что функция отправки вызвалась
        mock_send.assert_called_once()

        # Проверяем, что сообщение содержит правильный текст
        args, kwargs = mock_send.call_args
        self.assertEqual(args[0], "12345")  # telegram_chat_id
        self.assertIn("Тест привычка", args[1])  # сообщение
