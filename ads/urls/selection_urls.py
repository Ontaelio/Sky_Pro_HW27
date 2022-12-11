from django.urls import path

from ads import views

urlpatterns = [
    path('', views.SelectionListView.as_view(), name='Selections_view'),
    path('create/', views.SelectionCreateView.as_view(), name='Selection_create'),
    path('<int:pk>/', views.SelectionDetailView.as_view(), name='Selection_details'),
    path('<int:pk>/update/', views.SelectionUpdateView.as_view(), name='Selection_update'),
    path('<int:pk>/delete/', views.SelectionDeleteView.as_view(), name='Selection_delete'),
]
