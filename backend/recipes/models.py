from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from collections import defaultdict


class Recipe(models.Model):
    def get_nutrients(self, per_portion=True):

        totals = defaultdict(lambda: Decimal("0"))

        ingredients = self.ingredients.select_related("food").prefetch_related(
            "food__food_nutrients__nutrient"
        )

        for ingredient in ingredients:
            multiplier = Decimal(str(ingredient.serving_amount))

            for food_nutrient in ingredient.food.food_nutrients.all():
                totals[food_nutrient.nutrient] += food_nutrient.amount * multiplier

        if per_portion and self.portions:
            divisor = Decimal(str(self.portions))
            totals = {nutrient: amount / divisor for nutrient, amount in totals.items()}

        return totals

    def available_tags(self):
        return RecipeTag.objects.filter(user=self.user).exclude(recipes=self)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    name = models.CharField(max_length=255)
    is_favorite = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)

    summary = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    cooking_time = models.CharField(max_length=20, blank=True, null=True)
    portions = models.FloatField(
        default=1, help_text="Number of portions this recipe creates"
    )

    last_used_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField(
        "RecipeTag",
        related_name="recipes",
        blank=True,
    )

    def __str__(self):
        return self.name


class RecipePicture(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="pictures",
    )
    image = models.ImageField(upload_to="recipes/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "order"],
                name="unique_recipe_picture_order",
            ),
        ]

    def __str__(self):
        return f"{self.recipe.name} ({self.order})"


class RecipeTag(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipe_tags",
    )
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="ingredients"
    )

    food = models.ForeignKey("foods.Food", on_delete=models.CASCADE)

    default_servings = models.FloatField(default=1)
    serving_amount = models.FloatField(default=1)
    min_servings = models.FloatField(default=0)
    max_servings = models.FloatField(default=10)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):

        return f"{self.food.name} in {self.recipe.name}"
