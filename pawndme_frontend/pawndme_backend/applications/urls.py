from django.urls import path
from . import views

urlpatterns = [
    path('animals/<int:animal_id>/apply/', views.apply),
    path('applications/', views.application_list),
]