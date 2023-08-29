from rest_framework import viewsets, mixins
from .models import Notification, Modal
from .serializers import (
    NotificationSerializer,
    NotificationDetailSerializer,
    ModalSerializer,
)
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from datetime import datetime
from .paginations import NoticePagination


class NotificationViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    pagination_class = NoticePagination

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


class ModalViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ModalSerializer

    def get_queryset(self):
        today = datetime.now().date()

        queryset = Modal.objects.filter(
            Q(published_at__date__lte=today)
            & Q(ended_at__date__gte=today)
            & Q(is_active=True)
        ).order_by("-id")[:1]

        return queryset
