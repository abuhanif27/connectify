import pytest
from django.urls import reverse

from apps.accounts.models import User
from apps.conversations.models import (
    Conversation,
    ConversationParticipant,
    Message,
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

    charlie = User.objects.create_user(
        email="charlie@connectify.dev",
        password="StrongPassword123!",
    )

    return alice, bob, charlie


@pytest.fixture
def conversation(users):
    alice, bob, _ = users

    conversation = Conversation.objects.create(
        type=Conversation.ConversationType.DIRECT,
    )

    ConversationParticipant.objects.bulk_create(
        [
            ConversationParticipant(
                conversation=conversation,
                user=alice,
            ),
            ConversationParticipant(
                conversation=conversation,
                user=bob,
            ),
        ]
    )

    return conversation


@pytest.mark.django_db
def test_conversation_list_requires_authentication(client):
    url = reverse("conversations:list")

    response = client.get(url)

    assert response.status_code == 302
    assert "/auth/login/" in response.url


@pytest.mark.django_db
def test_authenticated_user_sees_their_conversations(
    client,
    users,
    conversation,
):
    alice, _, _ = users

    client.force_login(alice)

    url = reverse("conversations:list")
    response = client.get(url)

    assert response.status_code == 200
    assert conversation in response.context["conversations"]


@pytest.mark.django_db
def test_authenticated_user_does_not_see_other_users_conversations(
    client,
    users,
    conversation,
):
    alice, bob, charlie = users

    other_conversation = Conversation.objects.create(
        type=Conversation.ConversationType.DIRECT,
    )

    ConversationParticipant.objects.bulk_create(
        [
            ConversationParticipant(
                conversation=other_conversation,
                user=bob,
            ),
            ConversationParticipant(
                conversation=other_conversation,
                user=charlie,
            ),
        ]
    )

    client.force_login(alice)

    url = reverse("conversations:list")
    response = client.get(url)

    assert conversation in response.context["conversations"]
    assert other_conversation not in response.context["conversations"]


@pytest.mark.django_db
def test_participant_can_open_conversation(
    client,
    users,
    conversation,
):
    alice, _, _ = users

    client.force_login(alice)

    Message.objects.create(
        conversation=conversation,
        sender=alice,
        content="Hello Bob!",
    )

    url = reverse(
        "conversations:detail",
        kwargs={"conversation_id": conversation.id},
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.context["conversation"] == conversation
    assert response.context["messages"].count() == 1


@pytest.mark.django_db
def test_non_participant_cannot_open_conversation(
    client,
    users,
    conversation,
):
    _, _, charlie = users

    client.force_login(charlie)

    url = reverse(
        "conversations:detail",
        kwargs={"conversation_id": conversation.id},
    )

    response = client.get(url)

    assert response.status_code == 404
