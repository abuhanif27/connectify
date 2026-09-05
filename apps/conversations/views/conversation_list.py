from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.conversations.models import Conversation


User = get_user_model()


class ConversationListView(LoginRequiredMixin, TemplateView):
    template_name = "conversations/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        conversations = (
            Conversation.objects
            .filter(participants__user=user)
            .prefetch_related("participants__user")
            .distinct()
        )

        users = (
            User.objects
            .filter(is_active=True)
            .exclude(pk=user.pk)
            .order_by("first_name", "last_name", "email")
        )

        context["conversations"] = conversations
        context["users"] = users

        return context
