from django.urls import path

from .views import (
    HotelListView,
    HotelDetailView,
    MapView,
)

urlpatterns = [
    path("", HotelListView.as_view()),
    path("/<int:pk>", HotelDetailView.as_view()),
    path("/map", MapView.as_view()),
]
