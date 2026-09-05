from django.conf import settings
from django.db import models


class ConversationParticipant(models.Model):
    conversation = models.ForeignKey(
        "conversations.Conversation",
        on_delete=models.CASCADE,
        related_name="participants",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="conversation_participations",
    )

    joined_at = models.DateTimeField(
        auto_now_add=True,
    )

    last_read_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("conversation", "user"),
                name="unique_conversation_participant",
            ),
        ]
        ordering = ("joined_at",)

    def __str__(self):
        return f"{self.user.email} → {self.conversation}"
