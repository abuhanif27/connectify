from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.conversations.services import create_direct_conversation


User = get_user_model()


class CreateDirectConversationView(LoginRequiredMixin, View):
    def post(self, request):
        user_id = request.POST.get("user_id")

        user = get_object_or_404(
            User,
            pk=user_id,
            is_active=True,
        )

        if user == request.user:
            return redirect("conversations:list")

        conversation = create_direct_conversation(
            user_one=request.user,
            user_two=user,
        )

        return redirect(
            "conversations:detail",
            conversation_id=conversation.id,
        )
