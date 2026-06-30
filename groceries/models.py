from django.contrib.auth.models import User
from django.db import models

from foods.models import Food


class GroceryList(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="grocery_lists"
    )
    name = models.TextField()
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)

    # TODO what do auto now and auto add do?
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class GroceryListFood(models.Model):

    grocery_list = models.ForeignKey(
        GroceryList, on_delete=models.CASCADE, related_name="items"
    )

    food = models.ForeignKey(Food, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=8, decimal_places=2)

    on_hand = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.food.name
