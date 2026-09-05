import pytest
from django.urls import reverse

from apps.accounts.models import User
from apps.conversations.models import (
    Conversation,
    ConversationParticipant,
)


@pytest.fixture
def users():
    alice = User.objects.create_user(
        email="alice@connectify.dev",
        password="StrongPassword123!",
    )

    bob = User.objects.create_user(
        email="bob@connectify.dev",
        password="StrongPassword123!",
    )

    return alice, bob


@pytest.mark.django_db
def test_create_conversation_requires_authentication(client, users):
    _, bob = users

    url = reverse("conversations:create")

    response = client.post(
        url,
        {"user_id": bob.id},
    )

    assert response.status_code == 302
    assert "/auth/login/" in response.url


@pytest.mark.django_db
def test_user_can_create_direct_conversation(client, users):
    alice, bob = users

    client.force_login(alice)

    url = reverse("conversations:create")

    response = client.post(
        url,
        {"user_id": bob.id},
    )

    assert response.status_code == 302

    conversation = Conversation.objects.get(
        type=Conversation.ConversationType.DIRECT,
    )

    assert response.url == reverse(
        "conversations:detail",
        kwargs={"conversation_id": conversation.id},
    )

    assert ConversationParticipant.objects.filter(
        conversation=conversation,
        user=alice,
    ).exists()

    assert ConversationParticipant.objects.filter(
        conversation=conversation,
        user=bob,
    ).exists()


@pytest.mark.django_db
def test_existing_direct_conversation_is_reused(client, users):
    alice, bob = users

    client.force_login(alice)

    url = reverse("conversations:create")

    first_response = client.post(
        url,
        {"user_id": bob.id},
    )

    second_response = client.post(
        url,
        {"user_id": bob.id},
    )

    assert first_response.status_code == 302
    assert second_response.status_code == 302

    assert Conversation.objects.count() == 1
    assert first_response.url == second_response.url


@pytest.mark.django_db
def test_user_cannot_create_conversation_with_themselves(
    client,
    users,
):
    alice, _ = users

    client.force_login(alice)

    url = reverse("conversations:create")

    response = client.post(
        url,
        {"user_id": alice.id},
    )

    assert response.status_code == 302
    assert response.url == reverse("conversations:list")

    assert Conversation.objects.count() == 0


@pytest.mark.django_db
def test_invalid_user_returns_404(client, users):
    alice, _ = users

    client.force_login(alice)

    url = reverse("conversations:create")

    response = client.post(
        url,
        {"user_id": "00000000-0000-0000-0000-000000000000"},
    )

    assert response.status_code == 404
