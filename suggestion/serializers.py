from rest_framework import serializers
from .models import *


class SuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggestion
        fields = ["id", "content", "contact"]


class SuggestionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggestion
        fields = "__all__"
