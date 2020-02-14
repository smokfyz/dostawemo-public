from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from dostawemo.cities.models import Country, City
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True    

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given phone must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    phone = PhoneNumberField(default=None, null=True, blank=True, unique=True, verbose_name = 'Номер телефона')
    email = models.EmailField(_('email address'), default=None, null=True, unique=True, blank=True)
    birthday = models.DateField(null=True, blank=True, verbose_name = 'Дата рожденя')

    region = models.CharField(max_length=50, null=True, blank=True, verbose_name = 'Регион')
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name = 'Город')
    street = models.CharField(max_length=100, null=True, blank=True, verbose_name = 'Улица')
    house = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name = 'Дом')
    corpus = models.CharField(max_length=2, null=True, blank=True, verbose_name = 'Корпус')
    flat = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name = 'Квартира')
    zip_code = models.PositiveIntegerField(null=True, blank=True, verbose_name = 'Индекс')
    
    hobby = models.TextField(null=True, blank=True, verbose_name = 'Хобби')
    photo = models.ImageField(null=True, blank=True, upload_to='images/users/', verbose_name = 'Фото')

    bonus_points = models.PositiveIntegerField(default=0, verbose_name = 'Бонусные баллы')
    cashback_points = models.PositiveIntegerField(default=0, verbose_name = 'Кэшбэк')

    USERNAME_FIELD = 'email'
    USERNAME_FIELD_ADDITIONAL = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.phone)