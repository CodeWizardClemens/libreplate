from rest_framework import serializers

from .models import Unit


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = [
            "id",
            "name",
            "description",
            "abbreviation",
            "visible_in_nutrients",
            "visible_in_body_metrics",
            "visible_in_foods",
        ]
