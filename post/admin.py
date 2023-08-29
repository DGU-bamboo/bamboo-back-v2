from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from post.filters import PostTypeFilter
from post.models import Post, MaintainerPost
from report.models import MaintainerCommonReport, MaintainerNemoReport


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_filter = [PostTypeFilter]
    list_display = ["id", "type", "title"]
    search_fields = ["id", "content", "title"]


class MaintainerNemoReportInline(admin.TabularInline):
    model = MaintainerNemoReport
    show_change_link = True
    can_delete = False
    fields = ["content", "filtered_content"]
    readonly_fields = ["content", "filtered_content"]
    extra = 0

    def has_add_permission(self, request: HttpRequest, instance) -> bool:
        return False

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return (
            super().get_queryset(request).filter(type="NEMO", deleted_at__isnull=True)
        )


class MaintainerCommonReportInline(admin.TabularInline):
    model = MaintainerCommonReport
    show_change_link = True
    can_delete = False
    fields = ["content", "filtered_content"]
    readonly_fields = ["content", "filtered_content"]
    extra = 0

    def has_add_permission(self, request: HttpRequest, instance) -> bool:
        return False

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return (
            super().get_queryset(request).filter(type="COMMON", deleted_at__isnull=True)
        )


@admin.register(MaintainerPost)
class MaintainerPostAdmin(admin.ModelAdmin):
    readonly_fields = [
        "title",
        "type",
        "content",
        "created_at",
    ]
    exclude = [
        "deleted_at",
    ]
    search_fields = ["id", "content", "title"]
    list_filter = [PostTypeFilter]
    list_display = ["id", "type", "title"]
    inlines = [
        MaintainerNemoReportInline,
        MaintainerCommonReportInline,
    ]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).filter(deleted_at__isnull=True)
