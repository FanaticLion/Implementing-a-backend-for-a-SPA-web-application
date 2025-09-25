from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Профиль пользователя"""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
