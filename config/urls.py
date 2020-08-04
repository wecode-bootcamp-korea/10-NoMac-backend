from django.urls import (
    path,
    include
)

urlpatterns = [
    path("hotel", include("hotels.urls")),
]
