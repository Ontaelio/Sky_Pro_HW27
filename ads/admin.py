from django.contrib import admin

from ads.models import Category, Ad, Tag, Selection

admin.site.register(Ad)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Selection)