from django.urls import path, include
from .views import ReportViewSet
from rest_framework import routers

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("reports", ReportViewSet, basename="reports")


urlpatterns = [
    path("", include(default_router.urls)),
]
