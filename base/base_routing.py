from django.conf.urls import url
from base.base_consumers import GlobalWebsocket

websocket_urlpatterns = [
    # alterado de \w+ para [a-zA-Z0-9-_]+ para aceitar o nome do
    # channel concatenado ao ID do usuário(uuid)
    url(r'^ws/global/(?P<channel_code>[a-zA-Z0-9-_]+)/$',
        GlobalWebsocket.as_asgi()),
]
