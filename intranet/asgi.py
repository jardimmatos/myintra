import os

import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intranet.settings')
django.setup()

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
#django_asgi_app = get_asgi_application()

import base.base_routing
# import agenda.ws_routing
# import notifications.ws_routing
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            base.base_routing.websocket_urlpatterns# + 
            # agenda.ws_routing.websocket_urlpatterns +
            # notifications.ws_routing.websocket_urlpatterns
        )
    ),
})
