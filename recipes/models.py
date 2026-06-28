from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    name = models.CharField(max_length=255)
    thumbnail_path = models.CharField(max_length=500, blank=True, null=True)
    summary = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    portions = models.FloatField(
        default=1, help_text="Number of portions this recipe creates"
    )
    # last_used_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="ingredients"
    )

    food = models.ForeignKey("foods.Food", on_delete=models.CASCADE)

    # Current default amount used by recipe
    default_servings = models.FloatField(default=1)

    # Slider limits
    min_servings = models.FloatField(default=0)

    max_servings = models.FloatField(default=10)

    order = models.PositiveIntegerField(default=0)

    class Meta:

        ordering = ["order"]

    def __str__(self):

        return f"{self.food.name} " f"in {self.recipe.name}"
