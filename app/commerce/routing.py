from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/orders/<str:order_id>/', consumers.OrderConsumer.as_asgi()),
]