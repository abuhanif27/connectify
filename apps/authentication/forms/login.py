from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": (
                    "w-full rounded-xl border border-slate-700 "
                    "bg-slate-950 px-4 py-3 text-sm text-white "
                    "outline-none transition "
                    "placeholder:text-slate-600 "
                    "focus:border-indigo-500 "
                    "focus:ring-2 focus:ring-indigo-500/20"
                ),
                "placeholder": "you@example.com",
                "autocomplete": "email",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": (
                    "w-full rounded-xl border border-slate-700 "
                    "bg-slate-950 px-4 py-3 text-sm text-white "
                    "outline-none transition "
                    "placeholder:text-slate-600 "
                    "focus:border-indigo-500 "
                    "focus:ring-2 focus:ring-indigo-500/20"
                ),
                "placeholder": "Enter your password",
                "autocomplete": "current-password",
            }
        )
    )
