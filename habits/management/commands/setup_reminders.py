import json

from django.core.management.base import BaseCommand
from django_celery_beat.models import IntervalSchedule, PeriodicTask


class Command(BaseCommand):
    help = "Setup periodic tasks for habit reminders"

    def handle(self, *args, **options):
        # Создаем интервал - проверка каждую минуту
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.MINUTES,
        )

        # Создаем периодическую задачу
        task, created = PeriodicTask.objects.get_or_create(
            interval=schedule,
            name="Send habit reminders",
            task="habits.tasks.send_habit_reminders",
            defaults={
                "args": json.dumps([]),
                "kwargs": json.dumps({}),
                "enabled": True,
            },
        )

        if created:
            self.stdout.write(self.style.SUCCESS("Periodic task created successfully"))
        else:
            self.stdout.write(self.style.SUCCESS("Periodic task already exists"))
