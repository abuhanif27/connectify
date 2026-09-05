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

app_name = "conversations"

urlpatterns = [
    path("", ConversationListView.as_view(), name="list"),
    path(
        "<uuid:conversation_id>/",
        ConversationDetailView.as_view(),
        name="detail",
    ),
    path(
        "create/",
        CreateDirectConversationView.as_view(),
        name="create",
    ),
]
