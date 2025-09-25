from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Разрешение только для владельца объекта"""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsPublic(permissions.BasePermission):
    """Разрешение для публичных привычек"""

    def has_object_permission(self, request, view, obj):
        return obj.is_public
