from rest_framework import serializers
from .models import Notification, Modal
from django.utils.dateparse import parse_datetime


class NotificationSerializer(serializers.ModelSerializer):
    published_at = serializers.SerializerMethodField()

    def get_published_at(self, instance):
        return instance.published_at.strftime("%Y-%m-%d")

    class Meta:
        model = Notification
        fields = ["id", "image", "published_at"]


class NotificationDetailSerializer(serializers.ModelSerializer):
    published_at = serializers.SerializerMethodField()

    def get_published_at(self, instance):
        return instance.published_at.strftime("%Y-%m-%d %H:%M")

    class Meta:
        model = Notification
        fiedls = ["id", "title", "published_at", "image", "content", "url"]
        exclude = ["created_at", "updated_at", "deleted_at"]


class ModalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modal
        fields = ["id", "image", "published_at", "url"]
