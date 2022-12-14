import json

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from SkyPro_Homework_27 import settings
from ads.models import Ad, Tag
from ads.permissions import AdEditPermission
from ads.serializers import AdUpdateSerializer, AdDeleteSerializer
from ads.views.ad_filters import AD_FILTERS


def ad_as_dict(ad: Ad) -> dict:
    return {
        "id": ad.id,
        "name": ad.name,
        "author_id": ad.author.id,
        "author": ad.author.username,
        "price": str(ad.price),
        "description": ad.description,
        "is_published": ad.is_published,
        "category_id": ad.category.id,
        "category": ad.category.name,
        "image": ad.image.url if ad.image else None,
        "tags": list(map(str, ad.tags.all())),
        "location": ad.author.location.name,
    }


def filter_ads(ads_list, request):

    for r_field in AD_FILTERS.keys():
        if r_get := request.GET.get(r_field, None):
            ads_list = ads_list.filter(**{AD_FILTERS[r_field]: r_get})

    return ads_list


@method_decorator(csrf_exempt, name='dispatch')
class AdsView(ListView):
    model = Ad
    permission_required = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.select_related('author', 'author__location', 'category').prefetch_related(
            'tags').order_by('-price')

        self.object_list = filter_ads(self.object_list, request)

        total_ads = self.object_list.count()
        if not total_ads:
            return JsonResponse({'error': 'no ads found'}, status=404)

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
        # ad_item.image = ad_data.get("image", None)
        ad_item.is_published = False

        try:
            ad_item.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        ad_item.save()

        if tags := ad_data.get("tags"):
            for tag in tags:
                t, created = Tag.objects.get_or_create(name=tag)
                ad_item.tags.add(t)

        return JsonResponse(ad_as_dict(ad_item))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ad_detail_view(request, ad_num):
    try:
        ad = Ad.objects.get(pk=ad_num)
    except ObjectDoesNotExist:
        return JsonResponse({"error": f"Item {ad_num} not found"}, status=404)

    return JsonResponse(ad_as_dict(ad))


class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = [IsAuthenticated, AdEditPermission]


class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDeleteSerializer
    permission_classes = [IsAuthenticated, AdEditPermission]
    

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
