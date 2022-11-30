from django.contrib.auth.models import AbstractUser
from django.db import models


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

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    @property
    def location_txt(self):
        return self.location.name if self.location else None

