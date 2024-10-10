from django.urls import path
from apps.user.consumers import NotificationConsumer

websocket_urlpatterns = [
    path('ws/notifications/', NotificationConsumer.as_asgi()),
]