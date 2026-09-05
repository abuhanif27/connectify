from django.urls import path

from apps.conversations.views.conversation_detail import (
    ConversationDetailView,
)
from apps.conversations.views.conversation_list import (
    ConversationListView,
)
from apps.conversations.views.create_conversation import (
    CreateDirectConversationView,
)
from apps.conversations.views.send_message import (
    SendMessageView,
)


app_name = "conversations"

urlpatterns = [
    path("", ConversationListView.as_view(), name="list"),

    path(
        "create/",
        CreateDirectConversationView.as_view(),
        name="create",
    ),

    path(
        "<uuid:conversation_id>/messages/",
        SendMessageView.as_view(),
        name="send_message",
    ),

    path(
        "<uuid:conversation_id>/",
        ConversationDetailView.as_view(),
        name="detail",
    ),
]
