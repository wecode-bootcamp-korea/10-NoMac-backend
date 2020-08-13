from django.urls import path
from .views      import (
    ReviewView,
    StreamingView
)

urlpatterns = [
    path('',ReviewView.as_view()),
    path('/stream',StreamingView.as_view())
]