import pytest

from apps.accounts.models import User
from apps.conversations.models import (
    Conversation,
    ConversationParticipant,
    Message,
)
from apps.conversations.services import send_message


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
def test_participant_can_send_message(conversation, users):
    alice, _, _ = users

    message = send_message(
        conversation=conversation,
        sender=alice,
        content="Hello Bob!",
    )

    assert message.pk is not None
    assert message.sender == alice
    assert message.conversation == conversation
    assert message.content == "Hello Bob!"


@pytest.mark.django_db
def test_message_content_is_stripped(conversation, users):
    alice, _, _ = users

    message = send_message(
        conversation=conversation,
        sender=alice,
        content="   Hello Bob!   ",
    )

    assert message.content == "Hello Bob!"


@pytest.mark.django_db
def test_empty_message_is_rejected(conversation, users):
    alice, _, _ = users

    with pytest.raises(
        ValueError,
        match="Message content cannot be empty",
    ):
        send_message(
            conversation=conversation,
            sender=alice,
            content="   ",
        )

    assert Message.objects.count() == 0


@pytest.mark.django_db
def test_non_participant_cannot_send_message(conversation, users):
    _, _, charlie = users

    with pytest.raises(
        ValueError,
        match="Only conversation participants",
    ):
        send_message(
            conversation=conversation,
            sender=charlie,
            content="I should not be here.",
        )

    assert Message.objects.count() == 0


@pytest.mark.django_db
def test_sending_message_updates_conversation_activity(
    conversation,
    users,
):
    alice, _, _ = users

    old_updated_at = conversation.updated_at

    send_message(
        conversation=conversation,
        sender=alice,
        content="Hello Bob!",
    )

    conversation.refresh_from_db()

    assert conversation.updated_at > old_updated_at
