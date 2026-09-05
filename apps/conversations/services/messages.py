from django.db import transaction
from django.utils import timezone

from apps.accounts.models import User
from apps.conversations.models import Conversation, Message


@transaction.atomic
def send_message(
    *,
    conversation: Conversation,
    sender: User,
    content: str,
) -> Message:
    content = content.strip()

    if not content:
        raise ValueError("Message content cannot be empty.")

    is_participant = conversation.participants.filter(
        user=sender,
    ).exists()

    if not is_participant:
        raise ValueError(
            "Only conversation participants can send messages."
        )

    message = Message.objects.create(
        conversation=conversation,
        sender=sender,
        content=content,
    )

    Conversation.objects.filter(
        pk=conversation.pk,
    ).update(
        updated_at=timezone.now(),
    )

    return message
