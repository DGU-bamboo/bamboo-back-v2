from rest_framework import serializers
from report.models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["id", "type", "content", "password"]

    def create(self, validated_data):
        validated_data["filtered_content"] = validated_data["content"]
        return super().create(validated_data)
