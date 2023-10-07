from django.urls import path

from .consumer import NotificationConsumer

urlpatterns = [path("ws/notifications/", NotificationConsumer.as_asgi())]
