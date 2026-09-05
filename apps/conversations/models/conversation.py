import uuid

from django.db import models


class Conversation(models.Model):
    class ConversationType(models.TextChoices):
        DIRECT = "direct", "Direct"
        GROUP = "group", "Group"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    type = models.CharField(
        max_length=20,
        choices=ConversationType.choices,
        default=ConversationType.DIRECT,
    )

    title = models.CharField(
        max_length=255,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def get_display_name(self, current_user=None):
        if self.type == self.ConversationType.GROUP:
            return self.title or "Group conversation"

        if current_user is not None:
            other_participant = (
                self.participants
                .exclude(user=current_user)
                .select_related("user")
                .first()
            )

            if other_participant:
                user = other_participant.user

                full_name = user.get_full_name()

                if full_name:
                    return full_name

                return user.email

        return "Direct conversation"

    class Meta:
        ordering = ("-updated_at",)

    def __str__(self):
        if self.title:
            return self.title

        return f"{self.get_type_display()} conversation"
