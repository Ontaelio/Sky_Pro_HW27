from django.urls import path

from ads import views

urlpatterns = [
    path('', views.AdsView.as_view(), name='Ads_view'),
    path('<int:pk>/', views.AdDetailView.as_view(), name='Ad_view'),
    path('<int:pk>/update/', views.AdUpdateView.as_view(), name='Ad_update'),
    path('<int:pk>/delete/', views.AdDeleteView.as_view(), name='Ad_delete'),
    path('<int:pk>/upload_image/', views.AdImageView.as_view(), name='Ad_image_upload'),
]