from django.test import TestCase
from django.core.exceptions import ValidationError
from habits.models import Habit
from users.models import User


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='12:00:00',
            action='Приятная привычка',
            is_pleasant=True,
            time_to_complete=60
        )

    def test_habit_creation(self):
        habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='12:00:00',
            action='Читать книгу',
            time_to_complete=60
        )
        self.assertEqual(habit.action, 'Читать книгу')

    def test_time_to_complete_validation(self):
        """Тест валидации времени выполнения"""
        habit = Habit(
            user=self.user,
            place='Дом',
            time='12:00:00',
            action='Тест',
            time_to_complete=150  # > 120 секунд
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_related_habit_and_reward_validation(self):
        """Тест валидации связанной привычки и вознаграждения"""
        habit = Habit(
            user=self.user,
            place='Дом',
            time='12:00:00',
            action='Тест',
            related_habit=self.pleasant_habit,
            reward='Награда',
            time_to_complete=60
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_pleasant_habit_validation(self):
        """Тест валидации приятной привычки"""
        habit = Habit(
            user=self.user,
            place='Дом',
            time='12:00:00',
            action='Тест',
            is_pleasant=True,
            reward='Награда',  # Не должно быть у приятной привычки
            time_to_complete=60
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_habit_string_representation(self):
        """Тест строкового представления привычки"""
        habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='12:00:00',
            action='Тест привычка',
            time_to_complete=60
        )
        self.assertEqual(str(habit), f"{self.user.email}: Тест привычка")

    def test_related_habit_must_be_pleasant(self):
        """Тест что связанная привычка должна быть приятной"""
        unpleasant_habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='12:00:00',
            action='Неприятная привычка',
            is_pleasant=False,
            time_to_complete=60
        )

        habit = Habit(
            user=self.user,
            place='Дом',
            time='12:00:00',
            action='Тест',
            related_habit=unpleasant_habit,
            time_to_complete=60
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()