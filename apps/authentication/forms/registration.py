from django import forms

from apps.accounts.models import User


INPUT_CLASSES = (
    "w-full rounded-lg border border-gray-700 bg-gray-950 "
    "px-4 py-3 text-white outline-none transition "
    "placeholder:text-gray-500 "
    "focus:border-white focus:ring-1 focus:ring-white"
)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": INPUT_CLASSES,
                "placeholder": "Enter your password",
            }
        ),
        min_length=8,
    )

    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": INPUT_CLASSES,
                "placeholder": "Confirm your password",
            }
        ),
        min_length=8,
    )

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
        )

        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": INPUT_CLASSES,
                    "placeholder": "you@example.com",
                    "autocomplete": "email",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": INPUT_CLASSES,
                    "placeholder": "John",
                    "autocomplete": "given-name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": INPUT_CLASSES,
                    "placeholder": "Doe",
                    "autocomplete": "family-name",
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get(
            "password_confirmation"
        )

        if password and password_confirmation:
            if password != password_confirmation:
                self.add_error(
                    "password_confirmation",
                    "Passwords do not match.",
                )

        return cleaned_data
