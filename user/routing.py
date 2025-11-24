from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chatty/$', consumers.ChattyConsumer.as_asgi()),
]
