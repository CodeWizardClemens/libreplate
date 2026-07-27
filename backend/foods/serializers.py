from django.db import transaction
from rest_framework import serializers

from nutrients.models import Nutrient
from units.models import Unit

from .models import Food, FoodNutrient


class FoodNutrientSerializer(serializers.ModelSerializer):
    nutrient_id = serializers.PrimaryKeyRelatedField(
        queryset=Nutrient.objects.all(),
        source="nutrient",
    )

    nutrient_name = serializers.CharField(
        source="nutrient.name",
        read_only=True,
    )

    nutrient_unit = serializers.CharField(
        source="nutrient.unit",
        read_only=True,
    )

    class Meta:
        model = FoodNutrient
        fields = [
            "nutrient_id",
            "nutrient_name",
            "nutrient_unit",
            "amount",
        ]


class FoodSerializer(serializers.ModelSerializer):
    serving = serializers.FloatField()

    unit_id = serializers.PrimaryKeyRelatedField(
        queryset=Unit.objects.all(),
        source="unit",
    )

    unit_name = serializers.CharField(
        source="unit.name",
        read_only=True,
    )

    nutrients = FoodNutrientSerializer(
        many=True,
        required=False,
        source="food_nutrients",
    )

    class Meta:
        model = Food
        fields = [
            "id",
            "name",
            "serving",
            "unit_id",
            "unit_name",
            "barcode",
            "brand",
            "description",
            "is_favorite",
            "usda_fdc_id",
            "nutrients",
        ]

        read_only_fields = [
            "id",
            "unit_name",
        ]

    def _set_nutrients(self, food, nutrients):
        FoodNutrient.objects.filter(
            food=food
        ).delete()

        FoodNutrient.objects.bulk_create(
            [
                FoodNutrient(
                    food=food,
                    nutrient=item["nutrient"],
                    amount=item["amount"],
                )
                for item in nutrients
            ]
        )

    @transaction.atomic
    def create(self, validated_data):
        nutrients = validated_data.pop(
            "food_nutrients",
            [],
        )

        food = Food.objects.create(
            **validated_data
        )

        self._set_nutrients(
            food,
            nutrients,
        )

        return food

    @transaction.atomic
    def update(self, instance, validated_data):
        nutrients = validated_data.pop(
            "food_nutrients",
            None,
        )

        for attr, value in validated_data.items():
            setattr(
                instance,
                attr,
                value,
            )

        instance.save()

        if nutrients is not None:
            self._set_nutrients(
                instance,
                nutrients,
            )

        return instance