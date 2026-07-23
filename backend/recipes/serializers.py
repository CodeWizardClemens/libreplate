from rest_framework import serializers

from .models import (
    Recipe,
    RecipeTag,
    RecipeIngredient,
    RecipePicture,
)


class RecipeTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecipeTag
        fields = [
            "id",
            "name",
        ]


class RecipeIngredientSerializer(serializers.ModelSerializer):

    food_name = serializers.CharField(
        source="food.name",
        read_only=True,
    )

    class Meta:
        model = RecipeIngredient
        fields = [
            "id",
            "food",
            "food_name",
            "default_servings",
            "serving_amount",
            "min_servings",
            "max_servings",
            "order",
        ]


class RecipePictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecipePicture
        fields = [
            "id",
            "image",
        ]
        read_only_fields = [
            "id",
        ]


class RecipeSerializer(serializers.ModelSerializer):

    nutrients = serializers.SerializerMethodField()

    tags = RecipeTagSerializer(
        many=True,
        read_only=True,
    )

    picture = RecipePictureSerializer(
        read_only=True,
    )

    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=RecipeTag.objects.all(),
        source="tags",
        write_only=True,
        required=False,
    )

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
            "tag_ids",
            "picture",
            "nutrients",
        )

    def validate(self, attrs):

        request = self.context.get("request")

        if request and "tags" in attrs:

            tags = attrs["tags"]

            for tag in tags:

                if tag.user != request.user:
                    raise serializers.ValidationError(
                        {
                            "tag_ids": "You cannot use another user's tags."
                        }
                    )

        return attrs

    def get_nutrients(self, obj):

        nutrients = obj.get_nutrients()

        return [
            {
                "id": nutrient.id,
                "name": nutrient.name,
                "amount": amount,
            }
            for nutrient, amount in nutrients.items()
        ]