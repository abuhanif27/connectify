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
def test_send_message_requires_authentication(
    client,
    users,
    conversation,
):
    alice, _, _ = users

    url = reverse(
        "conversations:send_message",
        kwargs={"conversation_id": conversation.id},
    )

    response = client.post(
        url,
        {"content": "Hello Bob!"},
    )

    assert response.status_code == 302
    assert "/auth/login/" in response.url
    assert Message.objects.count() == 0


@pytest.mark.django_db
def test_participant_can_send_message(
    client,
    users,
    conversation,
):
    alice, _, _ = users

    client.force_login(alice)

    url = reverse(
        "conversations:send_message",
        kwargs={"conversation_id": conversation.id},
    )

    response = client.post(
        url,
        {"content": "Hello Bob!"},
    )

    assert response.status_code == 200
    assert Message.objects.count() == 1

    message = Message.objects.first()

    assert message.sender == alice
    assert message.conversation == conversation
    assert message.content == "Hello Bob!"
    assert "Hello Bob!" in response.content.decode()


@pytest.mark.django_db
def test_message_content_is_stripped(
    client,
    users,
    conversation,
):
    alice, _, _ = users

    client.force_login(alice)

    url = reverse(
        "conversations:send_message",
        kwargs={"conversation_id": conversation.id},
    )

    response = client.post(
        url,
        {"content": "   Hello Bob!   "},
    )

    assert response.status_code == 200

    message = Message.objects.first()

    assert message.content == "Hello Bob!"


@pytest.mark.django_db
def test_empty_message_is_rejected(
    client,
    users,
    conversation,
):
    alice, _, _ = users

    client.force_login(alice)

    url = reverse(
        "conversations:send_message",
        kwargs={"conversation_id": conversation.id},
    )

    response = client.post(
        url,
        {"content": "   "},
    )

    assert response.status_code == 404
    assert Message.objects.count() == 0


@pytest.mark.django_db
def test_non_participant_cannot_send_message(
    client,
    users,
    conversation,
):
    _, _, charlie = users

    client.force_login(charlie)

    url = reverse(
        "conversations:send_message",
        kwargs={"conversation_id": conversation.id},
    )

    response = client.post(
        url,
        {"content": "I should not be here."},
    )

    assert response.status_code == 404
    assert Message.objects.count() == 0
