from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.conversations.models import Conversation


class ConversationDetailView(LoginRequiredMixin, TemplateView):
    template_name = "conversations/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        conversation = get_object_or_404(
            Conversation,
            pk=self.kwargs["conversation_id"],
            participants__user=self.request.user,
        )

        messages = conversation.messages.select_related(
            "sender",
        )

        context["conversation"] = conversation
        context["messages"] = messages

        return context
