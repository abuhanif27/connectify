import pytest

from apps.accounts.models import User


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(
        email="john@example.com",
        password="StrongPassword123!",
        first_name="John",
        last_name="Doe",
    )

    assert user.email == "john@example.com"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.check_password("StrongPassword123!")
    assert user.is_active is True


@pytest.mark.django_db
def test_create_superuser():
    user = User.objects.create_superuser(
        email="admin@example.com",
        password="StrongPassword123!",
    )

    assert user.is_staff is True
    assert user.is_superuser is True
    assert user.is_active is True


@pytest.mark.django_db
def test_email_is_required():
    with pytest.raises(ValueError):
        User.objects.create_user(
            email="",
            password="StrongPassword123!",
        )


@pytest.mark.django_db
def test_user_string_representation():
    user = User.objects.create_user(
        email="john@example.com",
        password="StrongPassword123!",
    )

    assert str(user) == "john@example.com"
