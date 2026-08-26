from django.contrib.auth import authenticate


def authenticate_user(*, email: str, password: str):
    return authenticate(
        email=email,
        password=password,
    )
