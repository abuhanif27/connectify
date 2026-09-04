import pytest

from django.urls import reverse

from apps.accounts.models import User


@pytest.mark.django_db
def test_register_creates_user_and_logs_user_in(client):
    response = client.post(
        reverse("authentication:register"),
        {
            "email": "newuser@connectify.dev",
            "first_name": "New",
            "last_name": "User",
            "password": "StrongPassword123!",
            "password_confirmation": "StrongPassword123!",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("authentication:dashboard")

    user = User.objects.get(email="newuser@connectify.dev")

    assert user.first_name == "New"
    assert user.last_name == "User"
    assert client.session.get("_auth_user_id") == str(user.pk)


@pytest.mark.django_db
def test_login_with_valid_credentials(client):
    User.objects.create_user(
        email="login@connectify.dev",
        password="StrongPassword123!",
        first_name="Login",
        last_name="User",
    )

    response = client.post(
        reverse("authentication:login"),
        {
            "email": "login@connectify.dev",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("authentication:dashboard")


@pytest.mark.django_db
def test_login_with_invalid_credentials(client):
    User.objects.create_user(
        email="login@connectify.dev",
        password="StrongPassword123!",
    )

    response = client.post(
        reverse("authentication:login"),
        {
            "email": "login@connectify.dev",
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 200
    assert "Invalid email or password." in response.content.decode()


@pytest.mark.django_db
def test_dashboard_requires_authentication(client):
    response = client.get(
        reverse("authentication:dashboard")
    )

    assert response.status_code == 302
    assert response.url.startswith(
        reverse("authentication:login")
    )


@pytest.mark.django_db
def test_authenticated_user_can_access_dashboard(client):
    user = User.objects.create_user(
        email="dashboard@connectify.dev",
        password="StrongPassword123!",
        first_name="Dashboard",
        last_name="User",
    )

    client.force_login(user)

    response = client.get(
        reverse("authentication:dashboard")
    )

    assert response.status_code == 200
    assert b"Welcome to Connectify" in response.content
    assert b"Dashboard" in response.content


@pytest.mark.django_db
def test_logout_logs_user_out(client):
    user = User.objects.create_user(
        email="logout@connectify.dev",
        password="StrongPassword123!",
    )

    client.force_login(user)

    response = client.post(
        reverse("authentication:logout")
    )

    assert response.status_code == 302
    assert response.url == reverse("authentication:login")

    dashboard_response = client.get(
        reverse("authentication:dashboard")
    )

    assert dashboard_response.status_code == 302


@pytest.mark.django_db
def test_authenticated_user_is_redirected_from_login(client):
    user = User.objects.create_user(
        email="already@connectify.dev",
        password="StrongPassword123!",
    )

    client.force_login(user)

    response = client.get(
        reverse("authentication:login")
    )

    assert response.status_code == 302
    assert response.url == reverse("authentication:dashboard")


@pytest.mark.django_db
def test_authenticated_user_is_redirected_from_register(client):
    user = User.objects.create_user(
        email="already@connectify.dev",
        password="StrongPassword123!",
    )

    client.force_login(user)

    response = client.get(
        reverse("authentication:register")
    )

    assert response.status_code == 302
    assert response.url == reverse("authentication:dashboard")
