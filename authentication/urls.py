from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication import views

urlpatterns = [
    path('', views.UsersView.as_view(), name='Users_view'),
    path('create/', views.UserCreateView.as_view(), name='User_create'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='User_view'),
    path('<int:pk>/update/', views.UserUpdateView.as_view(), name='User_update'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='User_delete'),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    # path('<int:pk>/upload_image/', views.AdImageView.as_view(), name='Ad_image_upload'),
]