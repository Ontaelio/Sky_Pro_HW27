import json

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, DeleteView, UpdateView

from SkyPro_Homework_27 import settings
from ads.models import User, Location, Ad


def user_as_dict(user: User) -> dict:
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "password": user.password,
        "role": user.role,
        "age": user.age,
        "location_id": user.location_id,
        "location": user.location.name if user.location else None,
    }


@method_decorator(csrf_exempt, name='dispatch')
class UsersView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.select_related('location')
        #authors_qs = Ad.objects.annotate(ads=Count('author'))
        total_users = self.object_list.count()

        if page_number := request.GET.get("page", None):
            paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        else:
            paginator = Paginator(self.object_list, total_users)
        page_obj = paginator.get_page(page_number) if page_number else paginator.get_page(1)

        response = []
        for user in page_obj:
            a = user_as_dict(user)
            a['total_ads'] = user.ads.filter(is_published=True).count()
            response.append(a)

        return JsonResponse({
            "items": response,
            "total": page_obj.paginator.count,
            "num_pages": page_obj.paginator.num_pages,
        })

    def post(self, request):
        user_data = json.loads(request.body)

        user_item = User()
        try:
            user_item.first_name = user_data["first_name"]
            user_item.username = user_data["username"]
            user_item.password = user_data["password"]

        except KeyError:
            return JsonResponse({'error': 'invalid JSON data'}, status=400)

        user_item.last_name = user_data.get("last_name", "")
        user_item.age = user_data.get("age", None)
        user_item.location_id = user_data.get("location_id", None)

        try:
            user_item.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        user_item.save()

        return JsonResponse(user_as_dict(user_item))


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        return JsonResponse(user_as_dict(user))


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'password', 'role', 'age', 'location']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user_data = json.loads(request.body)

        self.object.first_name = user_data.get("first_name", self.object.first_name)
        self.object.last_name = user_data.get("last_name", self.object.last_name)
        self.object.username = user_data.get("username", self.object.username)
        self.object.password = user_data.get("password", self.object.password)
        self.object.location_id = user_data.get("location_id", self.object.location_id)
        self.object.role = user_data.get("role", self.object.role)
        self.object.age = user_data.get("age", self.object.age)
        self.object.save()

        return JsonResponse(user_as_dict(self.object))


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"})
