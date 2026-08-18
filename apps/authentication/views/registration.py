from django.shortcuts import redirect, render
from django.views import View

from apps.authentication.forms import RegistrationForm
from apps.authentication.services import register_user


class RegisterView(View):
    template_name = "authentication/register.html"

    def get(self, request):
        form = RegistrationForm()

        return render(
            request,
            self.template_name,
            {"form": form},
        )

    def post(self, request):
        form = RegistrationForm(request.POST)

        if form.is_valid():
            register_user(
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
            )

            return redirect("authentication:register")

        return render(
            request,
            self.template_name,
            {"form": form},
        )
