from django.urls import path
from .consumers import CommentConsumer

websocket_urlpatters = [

    path('ws/post/<str:id>',CommentConsumer)
]