from rest_framework import serializers

from .models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    nutrients = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "is_favorite",
            "is_pinned",
            "summary",
            "description",
            "instructions",
            "cooking_time",
            "portions",
            "last_used_at",
            "created_at",
            "updated_at",
            "tags",
            "nutrients",
        )

    def get_nutrients(self, obj):
        nutrients = obj.get_nutrients()

        # Convert {Nutrient: Decimal} -> JSON-serializable format
        return [
            {
                "id": nutrient.id,
                "name": nutrient.name,
                "amount": amount,
            }
            for nutrient, amount in nutrients.items()
        ]
