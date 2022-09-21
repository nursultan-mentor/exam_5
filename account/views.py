from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .models import Profile, User
from .serializers import RegisterSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save()
        if self.kwargs.get('is_sender') == 'sender':
            Profile.objects.create(user=user, is_sender=True)
        elif self.kwargs.get('is_sender') == 'buyer':
            Profile.objects.create(user=user, is_sender=False)
        else:
            user.delete()
            raise ValueError('is_sender must be either "sender" or "buyer"')
