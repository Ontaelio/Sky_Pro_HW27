from django.contrib import admin

from ads.models import Category, Ad, Tag

admin.site.register(Ad)
admin.site.register(Category)
admin.site.register(Tag)
