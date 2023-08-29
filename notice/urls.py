from django.urls import path, include
from .views import NotificationViewSet, ModalViewSet
from rest_framework import routers

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("notices", NotificationViewSet, basename="notices")

modal_router = routers.SimpleRouter(trailing_slash=False)
modal_router.register("modals", ModalViewSet, basename="modals")

urlpatterns = [
    path("", include(default_router.urls)),
    path("", include(modal_router.urls)),
]
