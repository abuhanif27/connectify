from django.db import transaction

from apps.accounts.models import User
from apps.conversations.models import (
    Conversation,
    ConversationParticipant,
)


@transaction.atomic
def create_direct_conversation(
    *,
    user_one: User,
    user_two: User,
) -> Conversation:
    if user_one == user_two:
        raise ValueError(
            "A direct conversation requires two different users."
        )

    conversation = (
        Conversation.objects
        .filter(
            type=Conversation.ConversationType.DIRECT,
            participants__user=user_one,
        )
        .filter(
            participants__user=user_two,
        )
        .first()
    )

    if conversation is not None:
        return conversation

    conversation = Conversation.objects.create(
        type=Conversation.ConversationType.DIRECT,
    )

    ConversationParticipant.objects.bulk_create(
        [
            ConversationParticipant(
                conversation=conversation,
                user=user_one,
            ),
            ConversationParticipant(
                conversation=conversation,
                user=user_two,
            ),
        ]
    )

    return conversation
