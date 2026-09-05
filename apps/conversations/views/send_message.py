from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views import View

from apps.conversations.models import Conversation
from apps.conversations.services import send_message


class SendMessageView(LoginRequiredMixin, View):
    template_name = "conversations/partials/message.html"

    def post(self, request, conversation_id):
        conversation = get_object_or_404(
            Conversation,
            pk=conversation_id,
            participants__user=request.user,
        )

        content = request.POST.get("content", "")

        try:
            message = send_message(
                conversation=conversation,
                sender=request.user,
                content=content,
            )
        except ValueError as exc:
            raise Http404(str(exc))

        return render(
            request,
            self.template_name,
            {"message": message},
        )
