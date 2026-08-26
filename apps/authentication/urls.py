from django.urls import path

from apps.authentication.views.dashboard import DashboardView
from apps.authentication.views.registration import RegisterView
from apps.authentication.views.login import LoginView

app_name = "authentication"

urlpatterns = [
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path(
        "dashboard/",
        DashboardView.as_view(),
        name="dashboard",
    ),
]
