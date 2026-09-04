from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views import View

from apps.authentication.forms.login import LoginForm
from apps.authentication.services.login import authenticate_user


class LoginView(View):
    template_name = "authentication/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("authentication:dashboard")

        form = LoginForm()

        return render(
            request,
            self.template_name,
            {"form": form},
        )

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("authentication:dashboard")

        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate_user(
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )

            if user is not None:
                login(request, user)

                return redirect("authentication:dashboard")

            form.add_error(
                None,
                "Invalid email or password.",
            )

        return render(
            request,
            self.template_name,
            {"form": form},
        )
