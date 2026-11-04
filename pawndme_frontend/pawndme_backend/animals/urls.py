from django.urls import path
from . import views

urlpatterns = [
    path('animals/', views.animal_list_create),
    path('animals/locations/', views.animal_locations),
    path('animals/<int:pk>/', views.animal_detail),
    path('animals/<int:pk>/status/', views.animal_status),
    path('my-animals/', views.my_animals),
    path('favorites/', views.favorite_list),
    path('favorites/<int:animal_id>/', views.favorite_toggle),
]