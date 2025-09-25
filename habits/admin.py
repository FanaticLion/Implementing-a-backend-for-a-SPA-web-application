from django import forms
from django.contrib import admin

from .models import Habit


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["time_to_complete"].required = True


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    form = HabitForm
    list_display = (
        "user",
        "action",
        "place",
        "time",
        "is_pleasant",
        "is_public",
        "created_at",
    )
    list_filter = ("is_pleasant", "is_public", "periodicity", "created_at")
    search_fields = ("action", "place", "user__username", "user__email")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Основная информация", {"fields": ("user", "action", "place", "time")}),
        ("Тип привычки", {"fields": ("is_pleasant", "related_habit", "reward")}),
        ("Настройки", {"fields": ("periodicity", "time_to_complete", "is_public")}),
        ("Даты", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
