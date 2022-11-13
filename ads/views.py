import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView

from ads.models import Category, Ad


def index(request):
    return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name='dispatch')
class CategoriesView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        response = []
        for category in self.object_list:
            response.append({
                "id": category.id,
                "name": category.name,
            })

        return JsonResponse(response, safe=False)

    def post(self, request):
        cat_data = json.loads(request.body)

        cat_item = Category()
        cat_item.name = cat_data["name"]

        try:
            cat_item.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        cat_item.save()

        return JsonResponse({
            "id": cat_item.id,
            "name": cat_item.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdsView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        response = []
        for ad in self.object_list:
            response.append({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published,
            })

        return JsonResponse(response, safe=False)

    def post(self, request):
        ad_data = json.loads(request.body)

        ad_item = Ad()
        ad_item.name = ad_data["name"]
        ad_item.author = ad_data["author"]
        ad_item.price = ad_data["price"]
        ad_item.description = ad_data["description"]
        ad_item.address = ad_data["address"]
        ad_item.is_published = False

        try:
            ad_item.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        ad_item.save()

        return JsonResponse({
            "id": ad_item.id,
            "name": ad_item.name,
            "author": ad_item.author,
            "price": ad_item.price,
            "description": ad_item.description,
            "address": ad_item.address,
            "is_published": ad_item.is_published,
        })


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published,
        })
