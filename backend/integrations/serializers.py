from foods.serializers import FoodSerializer
from rest_framework import serializers


class USDAFoodSearchSerializer(serializers.Serializer):
    term = serializers.CharField(
        max_length=100,
    )


class USDAFoodSearchResponseSerializer(serializers.Serializer):
    foods = FoodSerializer(
        many=True,
    )


class USDASaveSerializer(serializers.Serializer):
    fdc_id = serializers.IntegerField(
        min_value=1,
    )
