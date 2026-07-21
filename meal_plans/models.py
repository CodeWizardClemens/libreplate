from django.conf import settings
from django.db import models


class WeekDay(models.IntegerChoices):
    MONDAY = 0, "Monday"
    TUESDAY = 1, "Tuesday"
    WEDNESDAY = 2, "Wednesday"
    THURSDAY = 3, "Thursday"
    FRIDAY = 4, "Friday"
    SATURDAY = 5, "Saturday"
    SUNDAY = 6, "Sunday"


class MealPlan(models.Model):
    name = models.CharField(
        max_length=255,
        default="New Meal Plan",
    )
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="meal_plans",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_used_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Meal Plan"
        verbose_name_plural = "Meal Plans"

    def __str__(self):
        return self.name


class MealPlanFood(models.Model):
    meal_plan = models.ForeignKey(
        MealPlan,
        on_delete=models.CASCADE,
        related_name="foods",
    )

    meal = models.ForeignKey(
        "default_meals.DefaultMeal",
        on_delete=models.CASCADE,
        related_name="meal_plan_foods",
    )

    food = models.ForeignKey(
        "foods.Food",
        on_delete=models.CASCADE,
        related_name="meal_plan_entries",
    )

    day = models.PositiveSmallIntegerField(
        choices=WeekDay.choices,
    )

    serving_size = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_servings = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.food.name} - {self.get_day_display()} - {self.meal.name}"


class MealPlanRecipe(models.Model):
    meal_plan = models.ForeignKey(
        MealPlan,
        on_delete=models.CASCADE,
        related_name="recipes",
    )

    meal = models.ForeignKey(
        "default_meals.DefaultMeal",
        on_delete=models.CASCADE,
        related_name="meal_plan_recipes",
    )

    recipe = models.ForeignKey(
        "recipes.Recipe",
        on_delete=models.CASCADE,
        related_name="meal_plan_entries",
    )

    day = models.PositiveSmallIntegerField(
        choices=WeekDay.choices,
    )

    serving_size = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    number_of_servings = models.DecimalField(max_digits=10, decimal_places=2, default=1)

    def __str__(self):
        return f"{self.recipe.name} - {self.get_day_display()} - {self.meal.name}"
