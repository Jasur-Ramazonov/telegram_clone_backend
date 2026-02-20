from django.urls import path
from .views import (
    GetUserView,
    CreateChatView,
    MessageCreateView,
    MessageDestroyView,
    DestroyChatView,
    MessageUpdateView,
    MessageListView,
    ListChatView,
    SearchUsersView,
    CheckChatsView,
    CreateContactView,
    DestroyContactView,
)

urlpatterns = [
    # other urls
    path('get-user/',GetUserView.as_view()),
    path('search-users/',SearchUsersView.as_view()),
    # chat urls
    path('create-chat/',CreateChatView.as_view()),
    path('delete-chat/',DestroyChatView.as_view()),
    path('list-chat/',ListChatView.as_view()),
    path('check-chat/',CheckChatsView.as_view()),
    # message urls
    path('create-message/',MessageCreateView.as_view()),
    path('delete-message/<uuid:pk>/',MessageDestroyView.as_view()),
    path('update-message/<uuid:pk>/',MessageUpdateView.as_view()),
    path('list-message/<uuid:pk>/',MessageListView.as_view()),
#     Contact urls
    path('create-contact/',CreateContactView.as_view()),
    path('delete-contact/<uuid:pk>/',DestroyContactView.as_view()),
]