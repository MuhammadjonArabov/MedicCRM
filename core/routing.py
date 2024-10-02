from channels.security.websocket import AllowedHostsOriginValidator
from apps.user.middleware import AuthMiddleware
from .asgi import application as django_asgi_app
from channels.routing import ProtocolTypeRouter, URLRouter
from websockets import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket":
            AllowedHostsOriginValidator(
            AuthMiddleware(
                URLRouter(
                    websocket_urlpatterns
                )
            )
        )
    }
)
