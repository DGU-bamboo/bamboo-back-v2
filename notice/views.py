from rest_framework import viewsets, mixins

from .models import Notification, Modal
from .serializers import NotificationSerializer, NotificationDetailSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from datetime import datetime


class NotificationViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    def get_serializer_class(self):
        if self.action == "retrieve":
            return NotificationDetailSerializer
        return NotificationSerializer

    def get_queryset(self):
        today = datetime.now().date()
        queryset = Notification.objects.filter(
            Q(published_at__date__lte=today)
        ).order_by("-published_at")
        return queryset
