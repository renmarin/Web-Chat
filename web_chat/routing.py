from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/(?P<room_name>\w+)/$', consumers.WebChatConsumer.as_asgi()),
]


# from channels.routing import route
# from backend.consumers import ws_connect, ws_receive, ws_disconnect, msg_consumer
#
# channel_routing = [
#     route("websocket.connect", ws_connect),
#     route("websocket.receive", ws_receive),
#     route("websocket.disconnect", ws_disconnect),
#     route("chat", msg_consumer),
# ]