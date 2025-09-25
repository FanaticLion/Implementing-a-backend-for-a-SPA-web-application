from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "telegram_chat_id", "phone", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active")
    fieldsets = UserAdmin.fieldsets + (
        ("Дополнительная информация", {"fields": ("telegram_chat_id", "phone")}),
    )
