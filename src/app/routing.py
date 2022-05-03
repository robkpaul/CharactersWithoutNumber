from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path(r'ws/rolls/<int:room_name>', consumers.ChatConsumer.as_asgi(), name="roll_log")
]