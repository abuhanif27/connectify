import pytest

from apps.accounts.models import User
from apps.conversations.models import Conversation, ConversationParticipant

import pytest

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
        first_name="Alice",
        last_name="Smith",
    )

    bob = User.objects.create_user(
        email="bob@connectify.dev",
        password="StrongPassword123!",
        first_name="Bob",
        last_name="Jones",
    )

    return alice, bob


@pytest.mark.django_db
def test_create_direct_conversation():
    conversation = Conversation.objects.create(
        type=Conversation.ConversationType.DIRECT,
    )

    assert conversation.pk is not None
    assert conversation.type == Conversation.ConversationType.DIRECT
    assert conversation.title == ""


@pytest.mark.django_db
def test_add_participants_to_conversation():
    user_one = User.objects.create_user(
        email="alice@connectify.dev",
        password="StrongPassword123!",
    )

    user_two = User.objects.create_user(
        email="bob@connectify.dev",
        password="StrongPassword123!",
    )

    conversation = Conversation.objects.create(
        type=Conversation.ConversationType.DIRECT,
    )

    ConversationParticipant.objects.create(
        conversation=conversation,
        user=user_one,
    )

    ConversationParticipant.objects.create(
        conversation=conversation,
        user=user_two,
    )

    participant_users = list(
        conversation.participants.values_list(
            "user_id",
            flat=True,
        )
    )

    assert conversation.participants.count() == 2
    assert user_one.pk in participant_users
    assert user_two.pk in participant_users


@pytest.mark.django_db
def test_user_cannot_join_same_conversation_twice():
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

    with pytest.raises(Exception):
        ConversationParticipant.objects.create(
            conversation=conversation,
            user=user,
        )


@pytest.mark.django_db
def test_direct_conversation_display_name_uses_other_user(
    users,
):
    alice, bob = users

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

    assert conversation.get_display_name(alice) == (
        bob.get_full_name() or bob.email
    )
