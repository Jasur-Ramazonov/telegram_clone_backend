from django.urls import re_path
from .consumers import ChatConsumer

websocket_url_patterns = [
    re_path(r'chat/(?P<chat_id>[^/]+)/$', ChatConsumer.as_asgi()),
]

