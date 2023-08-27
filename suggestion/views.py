from rest_framework import viewsets, mixins
from .models import *
from .serializers import *
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response


class SuggestionViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Suggestion.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve", "memo"]:
            return SuggestionAdminSerializer
        else:
            return SuggestionSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve", "memo"]:
            return [IsAdminUser()]
        return []

    @action(methods=["POST"], detail=True)
    def memo(self, request, *args, **kwargs):
        suggestion = self.get_object()
        memo = request.data.get("memo")
        suggestion.memo = memo
        suggestion.save(update_fields=["memo"])
        serializer = self.get_serializer(suggestion)
        return Response(serializer.data)
