from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _


class ModlaActiveFilter(admin.SimpleListFilter):
    title = _("모달 활성화 관련 필터")
    parameter_name = "modal_active_filter"

    def lookups(self, request, model_admin):
        return (
            ("ACTIVE", _(" 1. 활성화된 모달")),
            ("INACTIVE", _(" 2. 비활성화된 모달")),
        )

    def queryset(self, request: Any, queryset):
        if self.value() == "ACTIVE":
            return queryset.filter(is_active=True)
        if self.value() == "INACTIVE":
            return queryset.filter(is_active=False)
