from django.urls import path

from ads import views

urlpatterns = [
    path('', views.CategoriesView.as_view(), name='Categories_view'),

    path('<int:pk>/', views.CategoryDetailView.as_view(), name='Category_view'),
    path('<int:pk>/update/', views.CategoryUpdateView.as_view(), name='Category_update'),
    path('<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='Category_delete'),
]