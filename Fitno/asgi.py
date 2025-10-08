"""
ASGI config for Fitno project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import Fitno.routing  # مسیریابی WebSocket

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Fitno.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            Fitno.routing.websocket_urlpatterns
        )
    ),
})
