from django.db.models import Q
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Habit
from .permissions import IsOwner, IsPublic
from .serializers import HabitListSerializer, HabitSerializer


class HabitPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100


class HabitViewSet(viewsets.ModelViewSet):
    pagination_class = HabitPagination

    """ViewSet для привычек"""

    def get_queryset(self):
        user = self.request.user

        if self.action == "public":
            # Для публичного списка - только публичные привычки других пользователей
            if user.is_authenticated:
                return Habit.objects.filter(is_public=True).exclude(user=user)
            else:
                return Habit.objects.filter(is_public=True)
        elif self.action == "list":
            # Для личного списка - привычки текущего пользователя
            return Habit.objects.filter(user=user)
        else:
            return Habit.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return HabitListSerializer
        return HabitSerializer

    def get_permissions(self):
        """Настраиваем права доступа в зависимости от действия"""
        if self.action == "public":
            permission_classes = [permissions.AllowAny]
        elif self.action in ["create", "list"]:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsOwner]

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["get"])
    def public(self, request):
        """Список публичных привычек"""
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
