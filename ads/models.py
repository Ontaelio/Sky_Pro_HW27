from django.db import models


class Ad(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.CharField(max_length=2000, blank=True)
    address = models.CharField(max_length=100)
    is_published = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(max_length=50)
