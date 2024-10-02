from django.urls import path

from websockets.consumers.statuschange import StatusChangeConsumer
from websockets.consumers.test import TestConsumer

websocket_urlpatterns = [
    path("ws/test/", TestConsumer.as_asgi()),
    path("ws/change/", StatusChangeConsumer.as_asgi()),
]
