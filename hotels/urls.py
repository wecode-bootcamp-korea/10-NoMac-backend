from django.urls import path

from . import views

urlpatterns = [
    path("main", views.HotelListViwe.as_view()),
]
