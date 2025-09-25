from django.test import TestCase
from rest_framework.exceptions import ValidationError

from habits.models import Habit
from habits.serializers import HabitSerializer
from users.models import User


class HabitSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="12:00:00",
            action="Приятная привычка",
            is_pleasant=True,
            time_to_complete=60,
        )

    def test_serializer_valid_data(self):
        """Тест валидных данных сериализатора"""
        data = {
            "place": "Офис",
            "time": "09:00:00",
            "action": "Работать",
            "time_to_complete": 90,
        }
        serializer = HabitSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_invalid_time_to_complete(self):
        """Тест невалидного времени выполнения"""
        data = {
            "place": "Офис",
            "time": "09:00:00",
            "action": "Работать",
            "time_to_complete": 150,  # > 120
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("time_to_complete", serializer.errors)

    def test_serializer_create_sets_user(self):
        """Тест что сериализатор автоматически устанавливает пользователя"""
        data = {
            "place": "Офис",
            "time": "09:00:00",
            "action": "Работать",
            "time_to_complete": 90,
        }

        # Создаем контекст с пользователем
        serializer = HabitSerializer(
            data=data, context={"request": type("Request", (), {"user": self.user})()}
        )
        self.assertTrue(serializer.is_valid())
        habit = serializer.save()
        self.assertEqual(habit.user, self.user)
