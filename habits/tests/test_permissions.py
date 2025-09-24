from django.test import TestCase
from habits.permissions import IsOwner, IsPublic
from habits.models import Habit
from users.models import User
from rest_framework.test import APIRequestFactory


class PermissionsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',  # Добавьте эту строку
            email='other@example.com',
            password='testpass123'
        )
        self.habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='12:00:00',
            action='Тест',
            time_to_complete=60
        )
        self.public_habit = Habit.objects.create(
            user=self.other_user,
            place='Парк',
            time='08:00:00',
            action='Публичная',
            time_to_complete=90,
            is_public=True
        )

    def test_is_owner_permission(self):
        """Тест permission IsOwner"""
        permission = IsOwner()
        request = self.factory.get('/')
        request.user = self.user

        # Владелец имеет доступ
        self.assertTrue(permission.has_object_permission(request, None, self.habit))

        # Чужой пользователь не имеет доступа
        request.user = self.other_user
        self.assertFalse(permission.has_object_permission(request, None, self.habit))

    def test_is_public_permission(self):
        """Тест permission IsPublic"""
        permission = IsPublic()
        request = self.factory.get('/')
        request.user = self.user

        # Публичная привычка доступна
        self.assertTrue(permission.has_object_permission(request, None, self.public_habit))

        # Непубличная привычка не доступна
        self.assertFalse(permission.has_object_permission(request, None, self.habit))