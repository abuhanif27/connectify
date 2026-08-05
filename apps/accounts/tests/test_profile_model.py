import pytest

from apps.accounts.models import User


@pytest.mark.django_db
def test_profile_created_automatically():
    user = User.objects.create_user(
        email="john@example.com",
        password="StrongPassword123!",
    )

    assert user.profile is not None
