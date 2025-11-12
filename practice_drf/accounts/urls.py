from django.urls import path
from .views import SignupView, LoginView, CustomTokenRefreshView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh-token/", CustomTokenRefreshView.as_view(), name="refresh-token"),
]
