from rest_framework.filters import BaseFilterBackend


class TypeFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        post_type = request.query_params.get("type")
        if post_type in ["COMMON", "NEMO", "ADMIN"]:
            return queryset.filter(type=post_type)
        return queryset
