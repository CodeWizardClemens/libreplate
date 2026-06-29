from django.contrib.auth.models import User
from django.db import models


class Food(models.Model):
    name = models.CharField(max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="foods")

    serving = models.DecimalField(max_digits=6, decimal_places=2)

    unit = models.ForeignKey(
        "units.Unit", on_delete=models.CASCADE, null=True, blank=True
    )

    thumbnail_path = models.CharField(max_length=500, blank=True, null=True)
    barcode = models.CharField(max_length=50, blank=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    last_used_at = models.DateTimeField(null=True, blank=True, db_index=True)

    usda_fdc_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        db_index=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Foods"
        indexes = [
            models.Index(fields=["barcode"]),
            models.Index(fields=["user", "brand"]),
        ]

    def __str__(self):
        return self.name

    def get_thumbnail_url(self):
        if self.thumbnail_path:
            from django.conf import settings

            return f"{settings.MEDIA_URL}{self.thumbnail_path}"
        return None


class FoodNutrient(models.Model):
    food = models.ForeignKey(
        Food, on_delete=models.CASCADE, related_name="food_nutrients"
    )

    nutrient = models.ForeignKey("nutrients.Nutrient", on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("food", "nutrient")
