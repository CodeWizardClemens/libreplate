from django.contrib.auth.models import User
from django.db import models


class Food(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="foods")
    serving = models.FloatField()
    unit = models.ForeignKey(
        "units.Unit", on_delete=models.CASCADE, null=True, blank=True
    )

    barcode = models.CharField(max_length=50, blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    tags = models.ManyToManyField(
        "FoodTag",
        related_name="foods",
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_used_at = models.DateTimeField(null=True, blank=True, db_index=True)
    is_favorite = models.BooleanField(default=False)

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
        return None


class FoodTag(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="food_tags",
    )
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"],
                name="unique_user_food_tag",
            )
        ]

    def __str__(self):
        return self.name


class FoodNutrient(models.Model):
    food = models.ForeignKey(
        Food, on_delete=models.CASCADE, related_name="food_nutrients"
    )

    nutrient = models.ForeignKey("nutrients.Nutrient", on_delete=models.CASCADE)

    amount = models.FloatField()

    class Meta:
        unique_together = ("food", "nutrient")
