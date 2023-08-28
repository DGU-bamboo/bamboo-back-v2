from django.urls import path, include
from .views import NotificationViewSet
from rest_framework import routers

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("notices", NotificationViewSet, basename="notices")

urlpatterns = [
    path("", include(default_router.urls)),
]
