from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from users.models import User  # Будем создавать кастомную модель пользователя


class Habit(models.Model):
    PERIOD_CHOICES = [
        ("daily", "Ежедневно"),
        ("weekly", "Еженедельно"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="habits",
    )
    place = models.CharField(
        max_length=255,
        verbose_name="Место выполнения",
        help_text="Место, в котором необходимо выполнять привычку",
    )
    time = models.TimeField(
        verbose_name="Время выполнения",
        help_text="Время, когда необходимо выполнять привычку",
    )
    action = models.CharField(
        max_length=500,
        verbose_name="Действие",
        help_text="Действие, которое представляет собой привычка",
    )
    is_pleasant = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки"
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
        help_text="Приятная привычка, связанная с полезной",
    )
    periodicity = models.CharField(
        max_length=10,
        choices=PERIOD_CHOICES,
        default="daily",
        verbose_name="Периодичность",
    )
    reward = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Вознаграждение",
        help_text="Чем пользователь должен себя вознаградить после выполнения",
    )
    time_to_complete = models.PositiveIntegerField(
        verbose_name="Время на выполнение (в секундах)",
        help_text="Время, которое предположительно потратит пользователь на выполнение привычки",
    )
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email}: {self.action}"

    def clean(self):
        """Валидация данных перед сохранением"""
        errors = {}

        # Валидация 1: Исключить одновременный выбор связанной привычки и указания вознаграждения
        if self.related_habit and self.reward:
            errors[
                "related_habit"
            ] = "Нельзя одновременно указывать связанную привычку и вознаграждение"
            errors[
                "reward"
            ] = "Нельзя одновременно указывать связанную привычку и вознаграждение"

        # Валидация 2: Время выполнения должно быть не больше 120 секунд
        if self.time_to_complete is not None and self.time_to_complete > 120:
            errors[
                "time_to_complete"
            ] = "Время выполнения не может превышать 120 секунд"

        # Валидация 3: В связанные привычки могут попадать только привычки с признаком приятной привычки
        if self.related_habit and not self.related_habit.is_pleasant:
            errors["related_habit"] = "Связанная привычка должна быть приятной"

        # Валидация 4: У приятной привычки не может быть вознаграждения или связанной привычки
        if self.is_pleasant:
            if self.reward:
                errors["reward"] = "У приятной привычки не может быть вознаграждения"
            if self.related_habit:
                errors[
                    "related_habit"
                ] = "У приятной привычки не может быть связанной привычки"

        if self.periodicity == "weekly":
            # Для еженедельной привычки проверяем, что она выполняется хотя бы раз в неделю
            # Это уже соответствует требованию, так как weekly = 1 раз в неделю
            pass
            # Если бы были другие варианты периодичности, нужно было бы добавить проверки

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Переопределяем save для вызова валидации"""
        self.clean()
        super().save(*args, **kwargs)
