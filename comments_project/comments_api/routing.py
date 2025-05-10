# from django.urls import re_path
# from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/comments/$', consumers.CommentConsumer.as_asgi()),
# ]


from django.urls import path
from comments_api.consumers import CommentConsumer

websocket_urlpatterns = [
    path("ws/comments/", CommentConsumer.as_asgi()),
]
