from django.contrib.auth.models import AbstractUser
from django.db import models

from authentication.models import User


class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Ad(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    author = models.ForeignKey(User, related_name='ads', on_delete=models.CASCADE, null=True, verbose_name='Автор')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    description = models.CharField(max_length=2000, blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name="Картинка")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, verbose_name="Категория")
    tags = models.ManyToManyField(Tag, verbose_name="Тэги")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'







