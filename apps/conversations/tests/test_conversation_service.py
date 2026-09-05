import pytest

from apps.accounts.models import User
from apps.conversations.models import (
    Conversation,
    ConversationParticipant,
)
from apps.conversations.services import create_direct_conversation


@pytest.mark.django_db
def test_create_direct_conversation():
    alice = User.objects.create_user(
        email="alice@connectify.dev",
        password="StrongPassword123!",
    )

    bob = User.objects.create_user(
        email="bob@connectify.dev",
        password="StrongPassword123!",
    )

    conversation = create_direct_conversation(
        user_one=alice,
        user_two=bob,
    )

    assert conversation.type == Conversation.ConversationType.DIRECT

    assert conversation.participants.count() == 2

    assert set(
        conversation.participants.values_list(
            "user_id",
            flat=True,
        )
    ) == {alice.pk, bob.pk}


@pytest.mark.django_db
def test_existing_direct_conversation_is_reused():
    alice = User.objects.create_user(
        email="alice@connectify.dev",
        password="StrongPassword123!",
    )

    bob = User.objects.create_user(
        email="bob@connectify.dev",
        password="StrongPassword123!",
    )

    first_conversation = create_direct_conversation(
        user_one=alice,
        user_two=bob,
    )

    second_conversation = create_direct_conversation(
        user_one=alice,
        user_two=bob,
    )

    assert first_conversation.pk == second_conversation.pk

    assert Conversation.objects.count() == 1


@pytest.mark.django_db
def test_direct_conversation_is_reused_regardless_of_user_order():
    alice = User.objects.create_user(
        email="alice@connectify.dev",
        password="StrongPassword123!",
    )

    bob = User.objects.create_user(
        email="bob@connectify.dev",
        password="StrongPassword123!",
    )

    first_conversation = create_direct_conversation(
        user_one=alice,
        user_two=bob,
    )

    second_conversation = create_direct_conversation(
        user_one=bob,
        user_two=alice,
    )

    assert first_conversation.pk == second_conversation.pk

    assert Conversation.objects.count() == 1


@pytest.mark.django_db
def test_user_cannot_create_direct_conversation_with_themselves():
    user = User.objects.create_user(
        email="alice@connectify.dev",
        password="StrongPassword123!",
    )

    with pytest.raises(
        ValueError,
        match="two different users",
    ):
        create_direct_conversation(
            user_one=user,
            user_two=user,
        )

    assert Conversation.objects.count() == 0
    assert ConversationParticipant.objects.count() == 0
