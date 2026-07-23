from rest_framework import serializers

from .models import Recipe, RecipeTag


class RecipeTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeTag
        fields = [
            "id",
            "name",
        ]


class RecipeSerializer(serializers.ModelSerializer):
    nutrients = serializers.SerializerMethodField()

    # Read: return full tag objects
    tags = RecipeTagSerializer(
        many=True,
        read_only=True,
    )

    # Write: accept tag IDs
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