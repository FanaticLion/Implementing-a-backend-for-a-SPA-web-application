from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from datetime import timedelta


class Command(BaseCommand):
    help = 'Setup periodic task for habit reminders'

    def handle(self, *args, **options):
        # Создаем интервал - проверка каждую минуту
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.MINUTES,
        )

        # Создаем периодическую задачу
        task, created = PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='Send habit reminders',
            task='habits.tasks.send_habit_reminders',
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS('Periodic task created successfully')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Periodic task already exists')
            )