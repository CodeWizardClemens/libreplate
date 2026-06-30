from rest_framework import serializers

from .models import GroceryList, GroceryListFood


class GroceryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroceryList
        fields = (
            "id",
            "date_start",
            "date_end",
            "generate_from_diary",
            "created_at",
            "updated_at",
        )


class GroceryListFoodSerializer(serializers.ModelSerializer):
    food_name = serializers.CharField(source="food.name", read_only=True)

    class Meta:
        model = GroceryListFood
        fields = (
            "id",
            "food",
            "food_name",
            "amount",
            "has_item",
        )
