from django.urls import path, include
from .views import *
from . import views
from rest_framework import routers
from .views import *

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("suggestions", SuggestionViewSet, basename="suggestions")


urlpatterns = [
    path("", include(default_router.urls)),
]
