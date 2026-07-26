from rest_framework import serializers


class USDAFoodSearchSerializer(serializers.Serializer):
    term = serializers.CharField(
        max_length=100
    )

    page_size = serializers.IntegerField(
        required=False,
        default=25,
        min_value=1,
        max_value=50,
    )

    page_number = serializers.IntegerField(
        required=False,
        default=1,
        min_value=1,
        max_value=1000,
    )


class USDASaveSerializer(serializers.Serializer):
    fdc_id = serializers.IntegerField(
        min_value=1
    )