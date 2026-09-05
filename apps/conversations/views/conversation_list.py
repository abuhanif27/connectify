from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.conversations.models import Conversation


class ConversationListView(LoginRequiredMixin, TemplateView):
    template_name = "conversations/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        conversations = (
            Conversation.objects
            .filter(participants__user=self.request.user)
            .prefetch_related("participants__user")
            .distinct()
        )

        context["conversations"] = conversations

        return context
