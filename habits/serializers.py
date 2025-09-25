from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "user_email",
            "place",
            "time",
            "action",
            "is_pleasant",
            "related_habit",
            "periodicity",
            "reward",
            "time_to_complete",
            "is_public",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["user", "created_at", "updated_at"]

    def validate(self, data):
        """Валидация данных на уровне сериализатора"""

        # Проверка: нельзя одновременно related_habit и reward
        if data.get("related_habit") and data.get("reward"):
            raise serializers.ValidationError(
                "Нельзя одновременно указывать связанную привычку и вознаграждение"
            )

        # Проверка: время выполнения <= 120 секунд
        if data.get("time_to_complete", 0) > 120:
            raise serializers.ValidationError(
                {"time_to_complete": "Время выполнения не может превышать 120 секунд"}
            )

        # Проверка: связанная привычка должна быть приятной
        related_habit = data.get("related_habit")
        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError(
                {"related_habit": "Связанная привычка должна быть приятной"}
            )

        # Проверка: у приятной привычки не может быть вознаграждения или связанной привычки
        if data.get("is_pleasant"):
            if data.get("reward"):
                raise serializers.ValidationError(
                    {"reward": "У приятной привычки не может быть вознаграждения"}
                )
            if data.get("related_habit"):
                raise serializers.ValidationError(
                    {
                        "related_habit": "У приятной привычки не может быть связанной привычки"
                    }
                )

        return data

    def create(self, validated_data):
        """Автоматически привязываем привычку к текущему пользователю"""
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class HabitListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка привычек"""

    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Habit
        fields = [
            "id",
            "user_email",
            "action",
            "place",
            "time",
            "is_pleasant",
            "is_public",
            "created_at",
        ]
