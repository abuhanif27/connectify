from django.db import transaction

from apps.accounts.models import User


@transaction.atomic
def register_user(
    *,
    email,
    password,
    first_name="",
    last_name="",
):
    user = User.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )

    return user
