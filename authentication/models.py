from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


def check_birth_date(value: date):
    if (value.year + 8, value.month, value.day) > (date.today().year, date.today().month, date.today().day):
        raise ValidationError('Must be at least 8 years of age to register')


class Location(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    lat = models.FloatField(null=True, blank=True, verbose_name="Широта")
    lng = models.FloatField(null=True, blank=True, verbose_name="Долгота")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
        ordering = ['id']


class User(AbstractUser):
    ROLES = [
        ('moderator', 'moderator'),
        ('admin', 'admin'),
        ('member', 'member'),
    ]

    role = models.CharField(max_length=10, default='member', verbose_name='Роль', choices=ROLES)
    age = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Возраст')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Место')
    birth_date = models.DateField(validators=[check_birth_date])
    email = models.EmailField(max_length=254, unique=True,
                              validators=[RegexValidator(regex=r"^(?i)[A-Za-z0-9._%+-]+@rambler\.ru$", inverse_match=True)])

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    @property
    def location_txt(self):
        return self.location.name if self.location else None
