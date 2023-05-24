from turtle import mode
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager, 
    PermissionsMixin
)
from common.contants import USER_TYPE
from common.custom_model import AbstractModel
from common.utils.image_progressive import create_thumbnail, has_changed


class CustomUserManager(BaseUserManager):

    def create_superuser(self, iin, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(iin, password, **extra_fields)

    def create_staff(self, iin, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self.create_user(iin, password, **extra_fields)

    def create_user(self, iin, password=None, **extra_fields):
        if not iin:
            raise ValueError("Нужен ИИН")
        if not password:
            raise ValueError("Нужен пароль")

        user = self.model(iin=iin, **extra_fields)
        user.set_password(password)
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, AbstractModel):
    iin = models.CharField(verbose_name='ИИН', max_length=12, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    surname = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(max_length=8, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.ImageField(verbose_name="Фото", null=True, blank=True, upload_to='avatar')
    user_type = models.PositiveIntegerField(choices=USER_TYPE, default=0)

    last_login = models.DateTimeField(auto_now_add=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'iin'
    REQUIRED_FIELDS = ['name', 'surname', 'birth_date', 'user_type']

    def __str__(self):
        return self.full_name
    
    @property
    def full_name(self):
        return f'{self.name} {self.surname}'

    def save(self, *args, **kwargs):
        if (has_changed(self, 'avatar')):
            self.avatar = create_thumbnail(self.avatar, 480)
        super(User, self).save(*args, **kwargs)
