import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, DeleteView, UpdateView

from ads.models import Ad


def index(request):
    return JsonResponse({"status": "ok"})


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
                "price": ad.price,
                "author": ad.author.username,
                "description": ad.description,
                "category": ad.category.name,
                "is_published": ad.is_published,
                "image": str(ad.image),
            })

        return JsonResponse(response, safe=False)

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

        return JsonResponse({
            "id": ad_item.id,
            "name": ad_item.name,
            "author": ad_item.author.username,
            "price": ad_item.price,
            "description": ad_item.description,
            "category": ad_item.category.name,
            "is_published": ad_item.is_published,
            "image": str(ad_item.image),
        })


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author.username,
            "price": ad.price,
            "description": ad.description,
            "category": ad.category.name,
            "is_published": ad.is_published,
            "image": str(ad.image),
        })


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
        self.object.author = cat_data.get("author_id", self.object.author)
        self.object.category = cat_data.get("category_id", self.object.category)
        self.object.is_published = cat_data.get("is_published", self.object.is_published)
        self.object.image = cat_data.get("image", self.object.image)
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author.id,
            "author": self.object.author.username,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category.id,
            "image": str(self.object.image),
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"})
