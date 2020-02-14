from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken, UntypedToken
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework_simplejwt.serializers import (
    PasswordField,
    TokenObtainSerializer,
    TokenObtainPairSerializer,
)
from random import randrange
import requests


User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    photo = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = User
        fields = [
            'url',
            'phone',
            'birthday',
            'hobby',
            'photo',
            'bonus_points',
            'cashback_points',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'groups'
        ]

    def get_image_url(self, obj):
        if obj.photo:
            return "http://" + self.context['request'].get_host() + "/" + obj.photo.url
        else:
            return None


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class PhoneSerializer(serializers.Serializer):
    phone = PhoneNumberField()

    def save(self):
        phone = self.validated_data['phone']
        random_code = str(randrange(100000, 1000000, 1))
        user, created = User.objects.get_or_create(phone=phone)
        user.set_password(random_code)
        user.save()
        res = requests.get(url="https://sms.ru/sms/send", params={
            "api_id": settings.API_SMS,
            "to": str(phone),
            "msg": "Code: %s" %random_code,
            "json": "1"
        })
        res = res.json()
        if 'balance' in res:
            del res['balance']
        return res


class CustomTokenObtainSerializer(TokenObtainSerializer):
    username_field = User.USERNAME_FIELD_ADDITIONAL

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['code'] = PasswordField()
        del self.fields['password']

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['code'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if self.user is None or not self.user.is_active:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        return {}


class CustomTokenObtainPairSerializer(CustomTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data
