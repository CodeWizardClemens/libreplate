import logging
from typing import Final

from django.db import transaction
from rest_framework import serializers

from integrations.usda_client import USDAFood, USDAFoodNutrient
from nutrients.models import Nutrient
from units.models import Unit

from .models import Food, FoodNutrient

logger = logging.getLogger(__name__)


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

    def to_representation(self, instance):

        if isinstance(instance, USDAFood):
            return self._serialize_usda_food(instance)

        return super().to_representation(instance)

    def _serialize_usda_food(self, food: USDAFood):

        try:
            GRAM: Final = Unit.objects.get(name="Gram")
        except Unit.DoesNotExist:
            raise ValueError("Required unit 'Gram' does not exist.")

        return {
            "id": None,
            "name": food.name,
            "serving": food.serving,
            "unit_id": GRAM.id,
            "unit_name": GRAM.name,
            "barcode": None,
            "brand": food.brand,
            "description": food.description,
            "is_favorite": False,
            "usda_fdc_id": food.fdc_id,
            "nutrients": self._serialize_usda_nutrients(
                food.food_nutrients,
            ),
        }

    def _serialize_usda_nutrients(self, usda_nutrients: list[USDAFoodNutrient]):
        """
        Serialize USDA nutrients into the application's nutrient format.

        Not all USDA nutrients are supported. Only nutrients that exist in the
        database are included in the serialized output; unsupported nutrients are
        ignored.
        """
        usda_nutrient_map = {
            nutrient.number: nutrient
            for nutrient in usda_nutrients
            if nutrient.number is not None
        }

        global_nutrients = {
            nutrient.usda_nutrient_number: nutrient
            for nutrient in Nutrient.objects.filter(
                usda_nutrient_number__in=usda_nutrient_map.keys(),
            )
        }

        return [
            {
                "nutrient_id": nutrient.id,
                "nutrient_name": nutrient.name,
                "nutrient_unit": nutrient.unit,
                "amount": usda_nutrient_map[nutrient.usda_nutrient_number].value,
            }
            for nutrient in global_nutrients.values()
        ]

    def _set_nutrients(self, food, nutrients):
        FoodNutrient.objects.filter(food=food).delete()

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

        food = Food.objects.create(**validated_data)

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
