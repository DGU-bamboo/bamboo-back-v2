from django.contrib import admin
from .models import Notification, Modal, MaintainerModal, MaintainerNotification
from notice.filters import ModlaActiveFilter


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "short_content"]
    search_fields = ["id", "content", "title"]

    def short_content(self, instance):
        return instance.content[:20]


@admin.register(Modal)
class ModalAdmin(admin.ModelAdmin):
    list_display = ["id", "is_active", "published_at"]
    search_fields = ["id"]
    list_filter = [ModlaActiveFilter]


@admin.register(MaintainerModal)
class MaintainerModalAdmin(admin.ModelAdmin):
    list_display = ["id", "is_active", "published_at"]
    search_fields = ["id"]
    list_filter = [ModlaActiveFilter]


@admin.register(MaintainerNotification)
class MaintainerNotificationAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "short_content"]
    search_fields = ["id", "content", "title"]

    def short_content(self, instance):
        return instance.content[:20]
