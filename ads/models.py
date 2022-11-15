from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Location(models.Model):
    name = models.CharField(max_length=150)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

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
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=15)
    role = models.CharField(max_length=10, default='member', choices=ROLES)
    age = models.PositiveSmallIntegerField(null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Ad(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.CharField(max_length=2000, blank=True, null=True)
    image = models.ImageField(upload_to='images/', null=True)
    is_published = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'







