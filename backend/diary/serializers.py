from django.db import transaction
from rest_framework import serializers

from foods.models import Food

from .models import Meal, MealFood
from foods.serializers import FoodSerializer


class MealFoodSerializer(serializers.ModelSerializer):
    food_id = serializers.PrimaryKeyRelatedField(
        queryset=Food.objects.all(),
        source="food",
        write_only=True,
    )

    food = FoodSerializer(read_only=True)

    class Meta:
        model = MealFood
        fields = [
            "id",
            "food_id",
            "food",
            "serving_size",
            "number_of_servings",
        ]
        read_only_fields = [
            "id",
            "food",
        ]

    def validate_food_id(self, food):
        request = self.context["request"]

        if food.user != request.user:
            raise serializers.ValidationError(
                "You cannot add foods belonging to another user."
            )

        return food


class MealSerializer(serializers.ModelSerializer):
    meal_foods = MealFoodSerializer(
        many=True,
        required=False,
    )

    class Meta:
        model = Meal
        fields = [
            "id",
            "name",
            "date",
            "note",
            "order",
            "meal_foods",
        ]
        read_only_fields = [
            "id",
        ]

    @transaction.atomic
    def create(self, validated_data):
        meal_foods = validated_data.pop("meal_foods", [])

        meal = Meal.objects.create(**validated_data)

        MealFood.objects.bulk_create(
            [
                MealFood(
                    meal=meal,
                    **meal_food,
                )
                for meal_food in meal_foods
            ]
        )

        return meal

    @transaction.atomic
    def update(self, instance, validated_data):
        meal_foods = validated_data.pop("meal_foods", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if meal_foods is not None:
            instance.meal_foods.all().delete()

            MealFood.objects.bulk_create(
                [
                    MealFood(
                        meal=instance,
                        **meal_food,
                    )
                    for meal_food in meal_foods
                ]
            )

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation["meal_foods"] = MealFoodSerializer(
            instance.meal_foods.select_related(
                "food",
                "food__unit",
            ).prefetch_related(
                "food__food_nutrients__nutrient"
            ),
            many=True,
            context=self.context,
        ).data

        return representation