import pytest

from apps.accounts.models import User
from apps.conversations.models import (
    Conversation,
    ConversationParticipant,
    Message,
)


@pytest.mark.django_db
def test_create_message():
    user = User.objects.create_user(
        email="alice@connectify.dev",
        password="StrongPassword123!",
    )

    conversation = Conversation.objects.create(
        type=Conversation.ConversationType.DIRECT,
    )

    ConversationParticipant.objects.create(
        conversation=conversation,
        user=user,
    )

    message = Message.objects.create(
        conversation=conversation,
        sender=user,
        content="Hello, Bob!",
    )

    assert message.pk is not None
    assert message.conversation == conversation
    assert message.sender == user
    assert message.content == "Hello, Bob!"


@pytest.mark.django_db
def test_conversation_messages_are_ordered_by_creation_time():
    user = User.objects.create_user(
        email="alice@connectify.dev",
        password="StrongPassword123!",
    )

    conversation = Conversation.objects.create(
        type=Conversation.ConversationType.DIRECT,
    )

    first_message = Message.objects.create(
        conversation=conversation,
        sender=user,
        content="First message",
    )

    second_message = Message.objects.create(
        conversation=conversation,
        sender=user,
        content="Second message",
    )

    messages = list(conversation.messages.all())

    assert messages == [
        first_message,
        second_message,
    ]


@pytest.mark.django_db
def test_deleting_conversation_deletes_messages():
    user = User.objects.create_user(
        email="alice@connectify.dev",
        password="StrongPassword123!",
    )

    conversation = Conversation.objects.create(
        type=Conversation.ConversationType.DIRECT,
    )

    message = Message.objects.create(
        conversation=conversation,
        sender=user,
        content="Hello!",
    )

    message_id = message.pk

    conversation.delete()

    assert not Message.objects.filter(pk=message_id).exists()
