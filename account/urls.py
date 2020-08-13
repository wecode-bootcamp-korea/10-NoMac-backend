from django.urls import path
from .views      import (
    SignUpView,
    SignInView,
    KakaoLoginView,
    GoogleLoginView
)

urlpatterns = [
    path('/sign-up',   SignUpView.as_view()),
    path('/sign-in/kakao', KakaoLoginView.as_view()),
    path('/sign-in/google', GoogleLoginView.as_view()),
    path('/sign-in',    SignInView.as_view()),
]