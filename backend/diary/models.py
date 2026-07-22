from django.contrib.auth.models import User
from django.db import models


class Meal(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    note = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meals")

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class MealFood(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="meal_foods")

    food = models.ForeignKey("foods.Food", on_delete=models.CASCADE)

    serving_size = models.FloatField()
    number_of_servings = models.FloatField()

    def __str__(self):
        return f"{self.food} ({self.number_of_servings}) in {self.meal}"
