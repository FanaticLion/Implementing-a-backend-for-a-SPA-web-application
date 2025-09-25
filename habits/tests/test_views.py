from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", email="other@example.com", password="testpass123"
        )

        self.habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="12:00:00",
            action="Личная привычка",
            time_to_complete=60,
        )

        self.public_habit = Habit.objects.create(
            user=self.other_user,
            place="Парк",
            time="08:00:00",
            action="Публичная привычка",
            time_to_complete=90,
            is_public=True,
        )

    def test_list_habits_authenticated(self):
        """Тест получения списка привычек авторизованным пользователем"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("habits-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_public_habits_list(self):
        """Тест получения публичных привычек"""
        response = self.client.get(reverse("habits-public"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_habit_authenticated(self):
        """Тест создания привычки авторизованным пользователем"""
        self.client.force_authenticate(user=self.user)
        data = {
            "place": "Спортзал",
            "time": "18:00:00",
            "action": "Тренировка",
            "time_to_complete": 90,
        }
        response = self.client.post(reverse("habits-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_own_habit(self):
        """Тест обновления своей привычки"""
        self.client.force_authenticate(user=self.user)
        data = {"action": "Обновленная привычка"}
        response = self.client.patch(
            reverse("habits-detail", args=[self.habit.id]), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_update_other_user_habit(self):
        """Тест невозможности обновления чужой привычки"""
        self.client.force_authenticate(user=self.other_user)
        data = {"action": "Попытка изменить"}
        response = self.client.patch(
            reverse("habits-detail", args=[self.habit.id]), data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_own_habit(self):
        """Тест удаления своей привычки"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse("habits-detail", args=[self.habit.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cannot_delete_other_user_habit(self):
        """Тест невозможности удаления чужой привычки"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(reverse("habits-detail", args=[self.habit.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
