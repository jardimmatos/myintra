from django.conf.urls import url
from base.base_consumers import MyWebsocket, MyWebsocket2, GlobalWebsocket
from notifications.consumers import NotificationsWebsocket
from agenda.consumers import AgendaLabsWebsocket

websocket_urlpatterns = [
    url(r'^ws/play/(?P<channel_code>\w+)/$', MyWebsocket.as_asgi()),
    url(r'^ws/play2/(?P<channel_code>\w+)/$', MyWebsocket2.as_asgi()),
    url(r'^ws/global/(?P<channel_code>[a-zA-Z0-9-_]+)/$', GlobalWebsocket.as_asgi()), # alterado de \w+ para [a-zA-Z0-9-_]+ para aceitar o nome do channel concatenado ao ID do usuário(uuid)
    url(r'^ws/notifications/(?P<channel_code>\w+)/$', NotificationsWebsocket.as_asgi()),
    url(r'^ws/agendalabs/(?P<channel_code>\w+)/$', AgendaLabsWebsocket.as_asgi()),
]