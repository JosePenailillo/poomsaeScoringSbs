from django.urls import path
from .consumers import EvaluationConsumer

websocket_urlpatterns = [
    path("ws/evaluaciones/", EvaluationConsumer.as_asgi()),
]