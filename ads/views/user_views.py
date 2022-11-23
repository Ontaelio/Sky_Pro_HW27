from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

from ads.models import User
from ads.serializers import UserListSerializer, UserCreateSerializer, UserUpdateSerializer, UserDeleteSerializer


# def user_as_dict(user: User) -> dict:
#     return {
#         "id": user.id,
#         "first_name": user.first_name,
#         "last_name": user.last_name,
#         "username": user.username,
#         "password": user.password,
#         "role": user.role,
#         "age": user.age,
#         "location_id": user.location_id,
#         "location": user.location.name if user.location else None,
#     }


class UsersView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDeleteSerializer

