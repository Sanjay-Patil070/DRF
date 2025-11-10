from django.urls import path, include
from .views import (
    EmployeeView,
    CreateEmployeeView,
    UpdateEmployeeView,
    DeleteEmployeeView,
    SignupView,
    LoginView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("get/employees/", EmployeeView.as_view(), name="get_employees"),
    path("create/employee/", CreateEmployeeView.as_view(), name="create_employee"),
    path(
        "update/employee/<int:employee_id>/",
        UpdateEmployeeView.as_view(),
        name="update_employee",
    ),
    path("delete/employee/", DeleteEmployeeView.as_view(), name="delete_employee"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
