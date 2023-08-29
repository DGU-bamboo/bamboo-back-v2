from typing import Any, List, Optional, Tuple
from django.contrib import admin
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _


class NemoApproveFilter(admin.SimpleListFilter):
    title = _("니모 제보 승인 관련 필터")
    parameter_name = "nemo_approve_filter"

    def lookups(self, request, model_admin):
        return (
            ("UPLOADED", _(" 1. 업로드된 니모")),
            ("NULL", _(" 2. 승인 확인이 필요한 니모")),
            ("APPROVED", _(" 3. 승인됐지만 게시되지 않은 니모")),
            ("REJECTED", _(" 4. 반려된 니모")),
        )

    def queryset(self, request: Any, queryset):
        if self.value() == "UPLOADED":
            return queryset.filter(post__isnull=False)
        if self.value() == "NULL":
            return queryset.filter(is_approved=None)
        if self.value() == "APPROVED":
            return queryset.filter(post__isnull=True, is_approved=True)
        if self.value() == "REJECTED":
            return queryset.filter(is_approved=False)


class CommonApproveFilter(admin.SimpleListFilter):
    title = _("일반 제보 승인 관련 필터")
    parameter_name = "common_approve_filter"

    def lookups(self, request, model_admin):
        return (
            ("UPLOADED", _(" 1, 업로드된 일반제보")),
            ("NULL", _(" 2. 승인 확인이 필요한 일반제보")),
            ("REJECTED", _(" 3. 반려된 일반제보")),
        )

    def queryset(self, request: Any, queryset):
        if self.value() == "UPLOADED":
            return queryset.filter(post__isnull=False)
        if self.value() == "NULL":
            return queryset.filter(is_approved=None)
        if self.value() == "REJECTED":
            return queryset.filter(is_approved=False)


class ReportFilter(admin.SimpleListFilter):
    title = _("제보 승인/타입 관련 필터")
    parameter_name = "report_apporve/type_filter"

    def lookups(self, request, model_admin):
        return (
            ("NEMO", _(" 1. 니모 제보")),
            ("COMMON", _(" 2. 일반 제보")),
            ("UPLOADED", _(" 3. 업로드된 제보")),
            ("NULL", _(" 4. 승인 확인이 필요한 제보")),
            ("APPROVED", _(" 5. 승인됐지만 게시되지 않은 니모")),
            ("REJECTED", _(" 6. 반려된 제보")),
        )

    def queryset(self, request: Any, queryset):
        if self.value() == "UPLOADED":
            return queryset.filter(post__isnull=False)
        if self.value() == "NULL":
            return queryset.filter(is_approved=None)
        if self.value() == "APPROVED":
            return queryset.filter(post__isnull=True, is_approved=True, type="NEMO")
        if self.value() == "REJECTED":
            return queryset.filter(is_approved=False)
        if self.value() == "NEMO":
            return queryset.filter(type="NEMO")
        if self.value() == "COMMON":
            return queryset.filter(type="COMMON")
