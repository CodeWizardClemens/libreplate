from rest_framework import serializers

from .models import Food, FoodNutrient


class FoodNutrientSerializer(serializers.ModelSerializer):
    nutrient_name = serializers.CharField(
        source="nutrient.name",
        read_only=True
    )
    nutrient_unit = serializers.CharField(
        source="nutrient.unit",
        read_only=True
    )

    class Meta:
        model = FoodNutrient
        fields = [
            "nutrient_name",
            "nutrient_unit",
            "amount",
        ]


class FoodSerializer(serializers.ModelSerializer):
    nutrients = FoodNutrientSerializer(
        source="food_nutrients",
        many=True,
        read_only=True
    )

    class Meta:
        model = Food
        fields = [
            "id",
            "name",
            "serving",
            "unit",
            "barcode",
            "brand",
            "description",
            "is_favorite",
            "usda_fdc_id",
            "nutrients",
        ]
        read_only_fields = [
            "id",
        ]