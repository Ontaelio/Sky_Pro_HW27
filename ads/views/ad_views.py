import json

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, DeleteView, UpdateView

from SkyPro_Homework_27 import settings
from ads.models import Ad


def ad_as_dict(ad: Ad) -> dict:
    return {
        "id": ad.id,
        "name": ad.name,
        "author_id": ad.author.id,
        "author": ad.author.username,
        "price": ad.price,
        "description": ad.description,
        "is_published": ad.is_published,
        "category_id": ad.category.id,
        "category": ad.category.name,
        "image": ad.image.url if ad.image else None,
    }


@method_decorator(csrf_exempt, name='dispatch')
class AdsView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.select_related('author', 'category').order_by('-price')
        total_ads = self.object_list.count()
        # self.object_list = self.object_list

        if page_number := request.GET.get("page", None):
            paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        else:
            paginator = Paginator(self.object_list, total_ads)
        page_obj = paginator.get_page(page_number) if page_number else paginator.get_page(1)

        ads = []
        for ad in page_obj:
            ads.append(ad_as_dict(ad))

        return JsonResponse({
            "items": ads,
            "total": page_obj.paginator.count,
            "num_pages": page_obj.paginator.num_pages,
        })

    def post(self, request):
        ad_data = json.loads(request.body)

        ad_item = Ad()

        try:
            ad_item.name = ad_data["name"]
            ad_item.author_id = ad_data["author_id"]
            ad_item.price = ad_data["price"]
            ad_item.category_id = ad_data["category_id"]
        except KeyError:
            return JsonResponse({'error': 'invalid JSON data'}, status=400)

        ad_item.description = ad_data.get("description", "")
        ad_item.image = ad_data.get("image", None)
        ad_item.is_published = False

        try:
            ad_item.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        ad_item.save()

        return JsonResponse(ad_as_dict(ad_item))


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse(ad_as_dict(ad))


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ['name', 'price', 'description', 'is_published', 'author', 'category']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        cat_data = json.loads(request.body)

        # if name := cat_data.get("name", None):
        #     self.object.name = name
        #     self.object.save()

        self.object.name = cat_data.get("name", self.object.name)
        self.object.price = cat_data.get("price", self.object.price)
        self.object.description = cat_data.get("description", self.object.description)
        self.object.author_id = cat_data.get("author_id", self.object.author_id)
        self.object.category_id = cat_data.get("category_id", self.object.category_id)
        self.object.is_published = cat_data.get("is_published", self.object.is_published)
        self.object.image = cat_data.get("image", self.object.image)
        self.object.save()

        return JsonResponse(ad_as_dict(self.object))


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = ['name', 'image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES["image"]
        self.object.save()

        return JsonResponse(ad_as_dict(self.object))


def index(request):
    return JsonResponse({"status": "ok"})
