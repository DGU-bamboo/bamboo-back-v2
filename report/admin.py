from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from report.filters import NemoApproveFilter, CommonApproveFilter, ReportFilter
from report.models import (
    Report,
    MaintainerNemoReport,
    MaintainerCommonReport,
)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_filter = [ReportFilter]
    list_display = [
        "id",
        "type",
        "short_content",
        "created_at",
        "is_approved",
    ]
    search_fields = ["filtered_content", "created_at"]

    def short_content(self, instance):
        return instance.content[:20]


@admin.register(MaintainerNemoReport)
class MaintainerNemoReportAdmin(admin.ModelAdmin):
    readonly_fields = [
        "content",
        "password",
        "type",
        "post",
    ]
    search_fields = ["filtered_content", "created_at", "content"]
    exclude = ["deleted_at"]
    list_filter = [NemoApproveFilter]
    list_display = ["id", "short_content", "created_at", "is_approved"]

    def short_content(self, instance):
        return instance.content[:20]

    def get_queryset(self, request):
        return (
            super().get_queryset(request).filter(type="NEMO", deleted_at__isnull=True)
        )


@admin.register(MaintainerCommonReport)
class MaintainerCommonReportAdmin(admin.ModelAdmin):
    readonly_fields = [
        "content",
        "password",
        "type",
        "post",
    ]
    search_fields = ["filtered_content", "created_at", "content"]
    exclude = ["deleted_at"]
    list_filter = [CommonApproveFilter]
    list_display = ["id", "short_content", "created_at", "is_approved"]

    def short_content(self, instance):
        return instance.content[:20]

    def get_queryset(self, request):
        return (
            super().get_queryset(request).filter(type="COMMON", deleted_at__isnull=True)
        )
