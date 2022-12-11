import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, DeleteView, UpdateView

from ads.models import Category


@method_decorator(csrf_exempt, name='dispatch')
class CategoriesView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by('name')

        response = []
        for category in self.object_list:
            response.append({
                "id": category.id,
                "name": category.name,
                "slug": category.slug,
            })

        return JsonResponse(response, safe=False)

    def post(self, request):
        cat_data = json.loads(request.body)

        cat_item = Category()
        cat_item.name = cat_data.get("name", None)
        if not cat_item.name:
            return JsonResponse({'error': 'name expected'}, status=400)

        cat_item.slug = cat_data.get("slug", None)
        if not cat_item.slug:
            return JsonResponse({'error': 'slug expected'}, status=400)

        try:
            cat_item.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        cat_item.save()

        return JsonResponse({
            "id": cat_item.id,
            "name": cat_item.name,
            "slug": cat_item.slug,
        })


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        cat_data = json.loads(request.body)

        if name := cat_data.get("name", None):
            self.object.name = name
            self.object.save()

        # if there will be more fields in future HWs, use these instead:

        # self.object.name = cat_data.get("name", self.object.name)
        # ...
        # self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"})
