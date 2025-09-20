from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    telegram_chat_id = models.CharField(
        max_length=30, 
        blank=True, 
        null=True, 
        verbose_name='Telegram Chat ID',
        help_text='ID чата в Telegram для отправки уведомлений'
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        return f"{self.username} ({self.email})"
