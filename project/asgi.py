"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# application = get_asgi_application()
import os

from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter

from channels.auth import AuthMiddlewareStack

from django.core.asgi import get_asgi_application

from interactions.routing import websocket_urlpatterns

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'project.settings'
)

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({

    "http": django_asgi_app,

    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),

})