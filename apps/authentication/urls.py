from django.urls import path

from apps.authentication.views.registration import RegisterView


app_name = "authentication"

urlpatterns = [
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),
]
