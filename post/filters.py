from rest_framework.filters import BaseFilterBackend
from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _


class TypeFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        post_type = request.query_params.get("type")
        if post_type in ["COMMON", "NEMO", "ADMIN"]:
            return queryset.filter(type=post_type)
        return queryset

class PostTypeFilter(admin.SimpleListFilter):
    title = _("게시글 타입 관련 필터")
    parameter_name = "post_type_filter"

    def lookups(self, request, model_admin):
        return (
            ("NEMO", _(" 1. 니모 제보 게시글")),
            ("COMMON", _(" 2. 일반 제보 게시글")),
        )

    def queryset(self, request: Any, queryset):
        if self.value() == "NEMO":
            return queryset.filter(type="NEMO")
        if self.value() == "COMMON":
            return queryset.filter(type="COMMON")

