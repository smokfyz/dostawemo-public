from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, generics, permissions, serializers, status
from dostawemo.users.serializers import UserSerializer, GroupSerializer, CustomTokenObtainPairSerializer, PhoneSerializer
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import (
    TokenViewBase,
)
from rest_framework.exceptions import APIException
import requests


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    @action(methods=['post'], detail=True)
    def image(self, request, pk=None):
        try:
            file = request.data['image']
        except KeyError:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        user = self.request.user
        user.photo = file
        user.save()
        return Response({}, status=status.HTTP_200_OK)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class SendCode(generics.CreateAPIView):
    """
    Send verification code to phone number. Create new user or use exiting.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = PhoneSerializer

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        res = self.perform_create(serializer)
        print(res)
        return Response(data=res, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = CustomTokenObtainPairSerializer