from django.db import models


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


class Location(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    lat = models.FloatField(null=True, blank=True, verbose_name="Широта")
    lng = models.FloatField(null=True, blank=True, verbose_name="Долгота")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


class User(models.Model):
    ROLES = [
        ('moderator', 'moderator'),
        ('admin', 'admin'),
        ('member', 'member'),
    ]
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия', blank=True)
    username = models.CharField(max_length=15, verbose_name='Имя_пользователя')
    password = models.CharField(max_length=15, verbose_name='Пароль')
    role = models.CharField(max_length=10, default='member', verbose_name='Роль', choices=ROLES)
    age = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Возраст')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Место')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']


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







