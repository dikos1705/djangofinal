from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from user.models import User
from user.serializers import (UserInfoSerializer, UserSerializer, UserUpdateSerializer)
from rest_framework.permissions import *

class UserView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get_serializer_class(self):
        if not self.request.method == "GET":
            return UserUpdateSerializer
        return UserInfoSerializer

    def get_object(self):
        obj = self.request.user
        self.check_object_permissions(self.request, obj)
        return obj


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)